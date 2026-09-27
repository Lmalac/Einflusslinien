from model.beam import Beam, SupportType
from calculation.dof_mapping import (
    build_node_dofs,
    get_vertical_dof
)


def test_vertical_dof():

    beam = Beam()

    beam.add_span(6.0)

    beam.add_support(0.0, SupportType.PINNED)
    beam.add_support(6.0, SupportType.ROLLER)

    beam.add_internal_hinge(3.0)

    print("\n=== VERTICAL DOF ===")

    for node_index in range(len(beam.spans) + 1):

        node_dofs = build_node_dofs(
            beam,
            node_index
        )

        vertical_dof = get_vertical_dof(
            beam,
            node_index
        )

        print(
            f"Узел {node_index}: "
            f"DOF = {node_dofs}, "
            f"v = DOF {vertical_dof}"
        )

    assert build_node_dofs(beam, 0) == [0, 1]
    assert build_node_dofs(beam, 1) == [2, 3, 4]
    assert build_node_dofs(beam, 2) == [5, 6]

    assert get_vertical_dof(beam, 0) == 0
    assert get_vertical_dof(beam, 1) == 2
    assert get_vertical_dof(beam, 2) == 5

    print("\nПроверки пройдены.")


if __name__ == "__main__":
    test_vertical_dof()