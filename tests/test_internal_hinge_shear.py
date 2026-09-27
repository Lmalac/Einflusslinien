from model.beam import Beam, SupportType

from calculation.load import create_vertical_nodal_load
from calculation.boundary_conditions import find_node_index
from calculation.solver import solve_beam
from calculation.section_forces import calculate_shear_at_section


def test_internal_hinge_shear():

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

    print("\n=== ПОПЕРЕЧНАЯ СИЛА В СЕЧЕНИЯХ ===")

    test_positions = [
        (0.0, "right"),
        (1.5, "left"),
        (1.5, "right"),
        (3.0, "left"),
        (3.0, "right"),
        (4.5, "left"),
        (4.5, "right"),
        (6.0, "left"),
    ]

    for position, side in test_positions:

        shear = calculate_shear_at_section(
            beam,
            displacements,
            position,
            side
        )

        print(
            f"x = {position:.2f} м, "
            f"{side:>5}: "
            f"Q = {shear:.6f}"
        )


if __name__ == "__main__":
    test_internal_hinge_shear()