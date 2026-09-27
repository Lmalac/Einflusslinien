from model.beam import Beam, SupportType

from calculation.load import create_vertical_nodal_load
from calculation.boundary_conditions import (
    find_node_index,
    get_constrained_dofs
)
from calculation.dof_mapping import build_node_dofs
from calculation.solver import solve_beam


def test_internal_hinge_solution():

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

    beam.add_internal_hinge(3.0)

    beam.insert_node(1.5)

    load_node = find_node_index(
        beam,
        1.5
    )

    loads = create_vertical_nodal_load(
        beam,
        load_node,
        -1.0
    )

    displacements = solve_beam(
        beam,
        loads
    )

    print("\n=== РЕШЕНИЕ БАЛКИ С ВНУТРЕННИМ ШАРНИРОМ ===")

    print("\nЗакреплённые DOF:")
    print(get_constrained_dofs(beam))

    print("\nDOF узлов:")

    for node_index in range(len(beam.spans) + 1):

        dofs = build_node_dofs(
            beam,
            node_index
        )

        print(
            f"  Узел {node_index}: {dofs}"
        )

    print("\nНагрузки:")
    print(loads)

    print("\nПеремещения:")
    print(displacements)


if __name__ == "__main__":
    test_internal_hinge_solution()