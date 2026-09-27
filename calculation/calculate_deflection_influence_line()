import numpy as np

from model.beam import Beam

from calculation.boundary_conditions import find_node_index
from calculation.load import create_vertical_nodal_load
from calculation.solver import solve_beam
from calculation.dof_mapping import get_number_of_dofs
from calculation.section_deflection import (
    calculate_deflection_at_section
)


def calculate_deflection_from_unit_load(
    beam: Beam,
    load_position: float,
    section_position: float
) -> float:

    if (
        load_position < 0
        or load_position > beam.total_length
    ):

        raise ValueError(
            "Координата нагрузки находится вне балки."
        )

    if (
        section_position < 0
        or section_position > beam.total_length
    ):

        raise ValueError(
            "Координата сечения находится вне балки."
        )

    calculation_beam = beam.copy()

    if (
        load_position > 0
        and load_position < calculation_beam.total_length
    ):

        calculation_beam.insert_node(
            load_position
        )

    if (
        section_position > 0
        and section_position < calculation_beam.total_length
    ):

        calculation_beam.insert_node(
            section_position
        )

    load_node_index = find_node_index(
        calculation_beam,
        load_position
    )

    number_of_dofs = get_number_of_dofs(
        calculation_beam
    )

    loads = create_vertical_nodal_load(
        calculation_beam,
        load_node_index,
        -1.0
    )

    if len(loads) != number_of_dofs:

        raise ValueError(
            "Размер вектора нагрузок "
            "не соответствует количеству "
            "степеней свободы."
        )

    displacements = solve_beam(
        calculation_beam,
        loads
    )

    deflection = calculate_deflection_at_section(
        calculation_beam,
        displacements,
        section_position
    )

    return deflection


def calculate_deflection_influence_line(
    beam: Beam,
    section_position: float,
    number_of_points: int = 101
):

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

    values = []

    for load_position in positions:

        value = calculate_deflection_from_unit_load(
            beam=beam,
            load_position=float(load_position),
            section_position=section_position
        )

        values.append(
            value
        )

    return (
        positions,
        np.asarray(
            values,
            dtype=float
        )
    )