from model.beam import Beam, SupportType

from calculation.load import create_vertical_nodal_load
from calculation.boundary_conditions import find_node_index
from calculation.solver import solve_beam
from calculation.reactions import calculate_reactions
from calculation.dof_mapping import get_vertical_dof


def test_internal_hinge_reactions():

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

    reactions = calculate_reactions(
        beam,
        loads,
        displacements
    )




    print("\n=== РЕАКЦИИ БАЛКИ С ВНУТРЕННИМ ШАРНИРОМ ===")

    support_positions = [0.0, 3.0, 6.0]

    total_reaction = 0.0

    for position in support_positions:

        node_index = find_node_index(
            beam,
            position
        )

        vertical_dof = get_vertical_dof(
            beam,
            node_index
        )

        reaction = reactions[vertical_dof]

        total_reaction += reaction

        print(
            f"Опора x = {position:.2f} м: "
            f"R = {reaction:.6f}"
        )

    print(
        f"\nСумма реакций = {total_reaction:.6f}"
    )


if __name__ == "__main__":
    test_internal_hinge_reactions()