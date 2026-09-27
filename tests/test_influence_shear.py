import numpy as np

from model.beam import Beam, SupportType

from calculation.solver import solve_beam
from calculation.section_forces import calculate_shear_at_section
from calculation.load import create_vertical_nodal_load
from calculation.boundary_conditions import find_node_index


def calculate_shear_from_unit_load(
    beam: Beam,
    load_position: float,
    section_position: float,
    side: str
) -> float:

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

    load_node = find_node_index(
        calculation_beam,
        load_position
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

    return calculate_shear_at_section(
        calculation_beam,
        displacements,
        section_position,
        side=side
    )


def test_shear_influence_line():

    beam = Beam()

    beam.add_span(6.0)

    beam.add_support(
        0.0,
        SupportType.PINNED
    )

    beam.add_support(
        6.0,
        SupportType.ROLLER
    )

    load_positions = np.array([
        0.0,
        1.0,
        2.0,
        2.9,
        3.1,
        4.0,
        5.0,
        6.0
    ])

    print("\n=== ЛИНИЯ ВЛИЯНИЯ Q В СЕЧЕНИИ x=3 ===")

    for load_position in load_positions:

        q_left = calculate_shear_from_unit_load(
            beam,
            load_position,
            section_position=3.0,
            side="left"
        )

        q_right = calculate_shear_from_unit_load(
            beam,
            load_position,
            section_position=3.0,
            side="right"
        )

        print(
            f"x = {load_position:.2f} м: "
            f"Q_left = {q_left:.6f}, "
            f"Q_right = {q_right:.6f}"
        )


if __name__ == "__main__":
    test_shear_influence_line()