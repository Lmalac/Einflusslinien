import numpy as np

from model.beam import Beam
from calculation.solver import solve_beam
from calculation.section_forces import (
    calculate_shear_at_section
)
from calculation.boundary_conditions import find_node_index


def calculate_shear_from_unit_load(
    beam: Beam,
    load_position: float,
    section_position: float,
    side: str = "left"
) -> float:
    """
    Вычисляет поперечную силу Q
    в заданном сечении от единичной нагрузки.

    load_position     — положение единичной нагрузки.
    section_position  — координата рассматриваемого сечения.
    side              — "left" или "right".

    Единичная нагрузка направлена вниз:
        P = -1
    """

    if load_position < 0 or load_position > beam.total_length:
        raise ValueError(
            "Координата нагрузки находится вне балки."
        )

    if section_position < 0 or section_position > beam.total_length:
        raise ValueError(
            "Координата сечения находится вне балки."
        )

    if side not in ("left", "right"):
        raise ValueError(
            'Параметр side должен быть "left" или "right".'
        )

    calculation_beam = beam.copy()

    if (
        load_position > 0
        and load_position < calculation_beam.total_length
    ):
        calculation_beam.insert_node(load_position)

    if (
        section_position > 0
        and section_position < calculation_beam.total_length
    ):
        calculation_beam.insert_node(section_position)

    number_of_nodes = len(calculation_beam.spans) + 1
    number_of_dofs = number_of_nodes * 2

    loads = np.zeros(number_of_dofs)

    load_node_index = find_node_index(
        calculation_beam,
        load_position
    )

    load_dof = 2 * load_node_index

    loads[load_dof] = -1.0

    displacements = solve_beam(
        calculation_beam,
        loads
    )

    return calculate_shear_at_section(
        beam=calculation_beam,
        displacements=displacements,
        position=section_position,
        side=side
    )


def calculate_shear_influence_line(
    beam: Beam,
    section_position: float,
    number_of_points: int = 101,
    side: str = "left"
):
    """
    Строит линию влияния поперечной силы Q.

    Возвращает:
        positions — положение единичной нагрузки.
        values — ординаты линии влияния.
    """

    if number_of_points < 2:
        raise ValueError(
            "Количество точек должно быть не меньше 2."
        )

    if side not in ("left", "right"):
        raise ValueError(
            'Параметр side должен быть "left" или "right".'
        )

    positions = np.linspace(
        0.0,
        beam.total_length,
        number_of_points
    )

    values = []

    for position in positions:

        value = calculate_shear_from_unit_load(
            beam=beam,
            load_position=float(position),
            section_position=section_position,
            side=side
        )

        values.append(value)

    return positions, np.array(values)