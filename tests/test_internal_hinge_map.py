from model.beam import Beam, SupportType
from calculation.dof_mapping import (
    build_element_dof_map,
    build_node_dofs,
    get_number_of_dofs
)


def test_internal_hinge_map():

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

    print("\n=== КАРТА DOF ВНУТРЕННЕГО ШАРНИРА ===")

    print(
        f"Количество элементов: {len(beam.spans)}"
    )

    print(
        f"Общее количество DOF: "
        f"{get_number_of_dofs(beam)}"
    )

    print("\nУзлы:")

    current_position = 0.0

    for node_index in range(len(beam.spans) + 1):

        dofs = build_node_dofs(
            beam,
            node_index
        )

        print(
            f"  Узел {node_index}: "
            f"x = {current_position:.2f} м | "
            f"DOF = {dofs}"
        )

        if node_index < len(beam.spans):
            current_position += beam.spans[node_index].length

    print("\nЭлементы:")

    dof_map = build_element_dof_map(beam)

    for index, dofs in enumerate(dof_map):

        start = sum(
            span.length
            for span in beam.spans[:index]
        )

        end = start + beam.spans[index].length

        print(
            f"  Элемент {index + 1}: "
            f"{start:.2f} — {end:.2f} м | "
            f"DOF = {dofs}"
        )


if __name__ == "__main__":
    test_internal_hinge_map()