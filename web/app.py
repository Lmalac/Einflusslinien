from pathlib import Path
from contextlib import contextmanager
import sqlite3
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from model.beam import Beam, SupportType

from calculation.dof_mapping import (
    get_number_of_dofs,
    get_vertical_dof
)

from calculation.global_stiffness import (
    build_global_stiffness
)

from calculation.load import (
    create_vertical_nodal_load
)

from calculation.solver import (
    solve_beam
)

from calculation.reactions import (
    calculate_reactions
)

from calculation.boundary_conditions import (
    find_node_index
)
from calculation.influence import calculate_influence_line
from calculation.influence_data import prepare_influence_data


app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
ANALYTICS_DB = BASE_DIR / "analytics.sqlite3"


@contextmanager
def analytics_connection():
    connection = sqlite3.connect(ANALYTICS_DB, timeout=10)
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS visitors (
                visitor_id TEXT PRIMARY KEY
            )
            """
        )
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def register_visitor(visitor_id: str) -> None:
    with analytics_connection() as connection:
        connection.execute(
            "INSERT OR IGNORE INTO visitors (visitor_id) VALUES (?)",
            (visitor_id,),
        )


@app.middleware("http")
async def disable_ui_caching(request, call_next):
    response = await call_next(request)
    if request.url.path == "/" or request.url.path.startswith("/static/"):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


class SpanData(BaseModel):
    length: float
    relative_ei: float


class SupportData(BaseModel):
    position: float
    support_type: str


class HingeData(BaseModel):
    position: float


class SchemeData(BaseModel):
    spans: list[SpanData]
    supports: list[SupportData]
    internal_hinges: list[HingeData]


class InfluenceRequest(SchemeData):
    quantity: str
    position: float
    number_of_points: int = 101


@app.get("/")
def root(request: Request):
    visitor_id = request.cookies.get("beam_visitor_id") or str(uuid4())
    register_visitor(visitor_id)
    response = FileResponse(
        BASE_DIR / "templates" / "index.html"
    )
    response.set_cookie(
        "beam_visitor_id",
        visitor_id,
        max_age=60 * 60 * 24 * 365 * 2,
        httponly=True,
        samesite="lax",
        secure=request.url.scheme == "https",
    )
    return response


@app.get("/api/stats")
def get_site_stats():
    with analytics_connection() as connection:
        total_visitors = connection.execute(
            "SELECT COUNT(*) FROM visitors"
        ).fetchone()[0]
    return {"visitors": total_visitors}


def convert_support_type(
    support_type: str
) -> SupportType:

    mapping = {
        "pinned": SupportType.PINNED,
        "roller": SupportType.ROLLER,
        "fixed": SupportType.FIXED,
        "free": SupportType.FREE
    }

    if support_type not in mapping:
        raise ValueError(
            f"Неизвестный тип опоры: {support_type}"
        )

    return mapping[support_type]


def create_beam_from_data(
    data: SchemeData
) -> Beam:

    beam = Beam()

    for span in data.spans:

        beam.add_span(
            length=span.length,
            relative_ei=span.relative_ei
        )

    for support in data.supports:

        beam.add_support(
            position=support.position,
            support_type=convert_support_type(
                support.support_type
            )
        )

    for hinge in data.internal_hinges:

        beam.add_internal_hinge(
            position=hinge.position
        )

    return beam


@app.post("/api/build-scheme")
def build_scheme(
    data: SchemeData
):

    try:

        beam = create_beam_from_data(
            data
        )
        physical_span_count = len(beam.spans)

        # -------------------------------------------------
        # Тестовая единичная нагрузка.
        # Пока она автоматически располагается
        # в середине балки.
        # -------------------------------------------------

        load_position = (
            beam.total_length / 2
        )

        # Если нагрузка находится внутри пролёта,
        # создаём в этом месте узел.
        if (
            load_position > 0
            and load_position < beam.total_length
        ):

            beam.insert_node(
                load_position
            )

        # После добавления узла заново определяем
        # количество степеней свободы.
        number_of_dofs = get_number_of_dofs(
            beam
        )

        # -------------------------------------------------
        # Матрица жёсткости K
        # -------------------------------------------------

        stiffness_matrix = build_global_stiffness(
            beam
        )

        stiffness_matrix_size = [
            stiffness_matrix.shape[0],
            stiffness_matrix.shape[1]
        ]

        stiffness_matrix_data = (
            stiffness_matrix.tolist()
        )

        # -------------------------------------------------
        # Вектор нагрузки F
        # -------------------------------------------------

        load_node = find_node_index(
            beam,
            load_position
        )

        loads = create_vertical_nodal_load(
            beam,
            load_node,
            -1.0
        )

        load_vector = (
            loads.tolist()
        )

        # -------------------------------------------------
        # Решение K*u = F
        # -------------------------------------------------

        displacements = solve_beam(
            beam,
            loads
        )

        # -------------------------------------------------
        # Реакции опор
        # -------------------------------------------------

        reactions = calculate_reactions(
            beam,
            loads,
            displacements
        )

        support_reactions = []

        for support in beam.supports:

            support_node = find_node_index(
                beam,
                support.position
            )

            support_dof = get_vertical_dof(
                beam,
                support_node
            )

            support_reactions.append({
                "position": support.position,
                "value": float(
                    reactions[support_dof]
                )
            })

        # -------------------------------------------------
        # Ответ сервера
        # -------------------------------------------------

        return {
            "status": "ok",
            "message": "Расчётная схема создана.",

            "total_length": beam.total_length,

            "number_of_spans": physical_span_count,

            "number_of_supports": len(
                beam.supports
            ),

            "number_of_hinges": len(
                beam.internal_hinges
            ),

            "number_of_dofs": number_of_dofs,

            "stiffness_matrix_size":
                stiffness_matrix_size,

            "stiffness_matrix":
                stiffness_matrix_data,

            "load_vector":
                load_vector,

            "load_position":
                load_position,

            "support_reactions":
                support_reactions
        }

    except Exception as error:
        detail = str(error)
        headers = (
            {"X-Scheme-Status": "unstable"}
            if "изменяем" in detail.casefold() or "вырожден" in detail.casefold()
            else None
        )
        raise HTTPException(
            status_code=400,
            detail=detail,
            headers=headers,
        ) from error


@app.post("/api/influence")
def build_influence_line(data: InfluenceRequest):
    try:
        requested_quantity = data.quantity.strip().upper()
        quantity = "w" if requested_quantity == "W" else requested_quantity
        # В интерфейсе прогиб обозначен w; расчётное ядро называет его D.
        calculation_quantity = "D" if quantity == "w" else quantity
        if calculation_quantity not in {"R", "M", "Q", "D"}:
            raise ValueError("Выберите одну из величин R, M, Q или w.")
        if data.number_of_points < 2 or data.number_of_points > 1001:
            raise ValueError("Количество точек должно быть от 2 до 1001.")

        beam = create_beam_from_data(data)
        if not beam.spans:
            raise ValueError("Добавьте хотя бы один пролёт.")
        if calculation_quantity == "R" and not any(
            abs(s.position - data.position) < 1e-9 for s in beam.supports
        ):
            raise ValueError("Для линии влияния R выберите координату существующей опоры.")
        result = calculate_influence_line(
            beam, calculation_quantity, data.position, data.number_of_points
        )
        prepared = prepare_influence_data(result)
        prepared["quantity"] = quantity
        return {"status": "ok", **prepared, "target_position": data.position}
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
