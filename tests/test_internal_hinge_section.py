from model.beam import Beam, SupportType

from calculation.load import create_vertical_nodal_load
from calculation.boundary_conditions import find_node_index
from calculation.solver import solve_beam
from calculation.section_forces import calculate_moment_at_section


def test_internal_hinge_section():

    beam = Beam()

    beam.add_span(6.0)

    beam.add_support(
        0.0,
        SupportType.PINNED
    )

    beam.add_support(
        3.0,
        SupportType.ROLLER
    )

    beam.add_support(
        6.0,
        SupportType.ROLLER
    )

    beam.add_internal_hinge(3.0)

    beam.insert_node(1.5)

    loads = create_vertical_nodal_load(
        beam,
        find_node_index(beam, 1.5),
        -1.0
    )

    displacements = solve_beam(
        beam,
        loads
    )

    print("\n=== МОМЕНТЫ В СЕЧЕНИЯХ ===")

    for position in [0.0, 1.5, 3.0, 4.5, 6.0]:

        moment = calculate_moment_at_section(
            beam,
            displacements,
            position
        )

        print(
            f"x = {position:.2f} м: "
            f"M = {moment:.6f}"
        )


if __name__ == "__main__":
    test_internal_hinge_section()