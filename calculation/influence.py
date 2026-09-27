import numpy as np

from model.beam import Beam

from calculation.boundary_conditions import find_node_index
from calculation.load import create_vertical_nodal_load
from calculation.solver import solve_beam

from calculation.influence_response import (
    calculate_reaction_influence_line
)

from calculation.influence_moment import (
    calculate_moment_influence_line
)

from calculation.influence_deflection import (
    calculate_deflection_influence_line
)

from calculation.section_forces import (
    calculate_shear_at_section
)


def calculate_shear_influence_line(
    beam: Beam,
    section_position: float,
    number_of_points: int = 101
):
    """
    Строит линию влияния поперечной силы Q
    в заданном сечении.

    Возвращает:
        positions    — положения единичной нагрузки;
        left_values  — значения Q слева от сечения;
        right_values — значения Q справа от сечения.
    """

    if number_of_points < 2:
        raise ValueError(
            "Количество точек должно быть не меньше 2."
        )

    if (
        section_position < 0
        or section_position > beam.total_length
    ):
        raise ValueError(
            "Координата сечения находится вне балки."
        )

    positions = np.linspace(
        0.0,
        beam.total_length,
        number_of_points
    )

    left_values = []
    right_values = []

    for load_position in positions:

        calculation_beam = beam.copy()

        if (
            load_position > 0
            and load_position < calculation_beam.total_length
        ):
            calculation_beam.insert_node(
                float(load_position)
            )

        if (
            section_position > 0
            and section_position < calculation_beam.total_length
        ):
            calculation_beam.insert_node(
                section_position
            )

        load_node = find_node_index(
            calculation_beam,
            float(load_position)
        )

        loads = create_vertical_nodal_load(
            calculation_beam,
            load_node,
            -1.0
        )

        displacements = solve_beam(
            calculation_beam,
            loads
        )

        q_left = calculate_shear_at_section(
            calculation_beam,
            displacements,
            section_position,
            side="left"
        )

        q_right = calculate_shear_at_section(
            calculation_beam,
            displacements,
            section_position,
            side="right"
        )

        left_values.append(q_left)
        right_values.append(q_right)

    return (
        positions,
        np.asarray(left_values),
        np.asarray(right_values)
    )


def calculate_influence_line(
    beam: Beam,
    quantity: str,
    position: float,
    number_of_points: int = 101
):
    """
    Универсальный интерфейс для построения
    линии влияния.

    quantity:
        "R" — реакция опоры
        "M" — изгибающий момент
        "Q" — поперечная сила
        "D" — прогиб

    position:
        координата опоры или сечения.
    """

    quantity = quantity.upper()

    if quantity == "M":

        positions, values = calculate_moment_influence_line(
            beam=beam,
            section_position=position,
            number_of_points=number_of_points
        )

        return {
            "quantity": "M",
            "positions": positions,
            "values": values
        }

    if quantity == "R":

        positions = np.linspace(
            0.0,
            beam.total_length,
            number_of_points
        )

        values = calculate_reaction_influence_line(
            beam=beam,
            support_position=position,
            load_positions=positions
        )

        return {
            "quantity": "R",
            "positions": positions,
            "values": values
        }

    if quantity == "Q":

        positions, left_values, right_values = (
            calculate_shear_influence_line(
                beam=beam,
                section_position=position,
                number_of_points=number_of_points
            )
        )

        return {
            "quantity": "Q",
            "positions": positions,
            "left_values": left_values,
            "right_values": right_values
        }

    if quantity == "D":

        positions, values = calculate_deflection_influence_line(
            beam=beam,
            section_position=position,
            number_of_points=number_of_points
        )

        return {
            "quantity": "D",
            "positions": positions,
            "values": values
        }

    raise ValueError(
        'Неизвестная величина. Используйте "R", "M", "Q" или "D".'
    )