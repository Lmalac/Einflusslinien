import numpy as np

from model.beam import Beam, SupportType
from calculation.global_stiffness import build_global_stiffness
from calculation.dof_mapping import (
    build_node_dofs,
    build_element_dof_map,
    get_number_of_dofs
)
from calculation.boundary_conditions import get_constrained_dofs


def test_internal_hinge_dofs():

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

    beam.add_internal_hinge(
        3.0
    )

    K = build_global_stiffness(beam)

    print()
    print("=" * 60)
    print("ПРОВЕРКА ВНУТРЕННЕГО ШАРНИРА")
    print("=" * 60)

    print()
    print(
        f"Количество элементов: "
        f"{len(beam.spans)}"
    )

    print(
        f"Количество узлов: "
        f"{len(beam.spans) + 1}"
    )

    print(
        f"Количество DOF: "
        f"{get_number_of_dofs(beam)}"
    )

    print()
    print("DOF узлов:")

    for node_index in range(
        len(beam.spans) + 1
    ):

        dofs = build_node_dofs(
            beam,
            node_index
        )

        print(
            f"  Узел {node_index}: "
            f"DOF = {dofs}"
        )

    print()
    print("DOF элементов:")

    element_dof_map = build_element_dof_map(
        beam
    )

    for element_index, dofs in enumerate(
        element_dof_map
    ):

        print(
            f"  Элемент {element_index}: "
            f"DOF = {dofs}"
        )

    constrained = get_constrained_dofs(
        beam
    )

    print()
    print(
        f"Закреплённые DOF: "
        f"{constrained}"
    )

    print()
    print(
        f"Размер матрицы K: "
        f"{K.shape}"
    )

    print()
    print(
        f"Ранг полной матрицы K: "
        f"{np.linalg.matrix_rank(K)}"
    )

    all_dofs = np.arange(
        K.shape[0]
    )

    free_dofs = np.array([
        dof
        for dof in all_dofs
        if dof not in constrained
    ])

    Kff = K[
        np.ix_(
            free_dofs,
            free_dofs
        )
    ]

    print()
    print(
        f"Свободные DOF: "
        f"{free_dofs.tolist()}"
    )

    print(
        f"Размер Kff: "
        f"{Kff.shape}"
    )

    print(
        f"Ранг Kff: "
        f"{np.linalg.matrix_rank(Kff)}"
    )

    print()
    print("=" * 60)
    print("ТЕСТ ЗАВЕРШЁН")
    print("=" * 60)


if __name__ == "__main__":
    test_internal_hinge_dofs()