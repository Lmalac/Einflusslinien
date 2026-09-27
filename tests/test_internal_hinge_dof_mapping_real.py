from model.beam import Beam, SupportType
from calculation.dof_mapping import (
    build_element_dof_map,
    get_number_of_dofs
)


def test_internal_hinge_dof_mapping_real():

    beam = Beam()

    beam.add_span(6.0)

    beam.add_support(0.0, SupportType.PINNED)
    beam.add_support(6.0, SupportType.ROLLER)

    beam.add_internal_hinge(3.0)

    dof_map = build_element_dof_map(beam)
    number_of_dofs = get_number_of_dofs(beam)

    print("\n=== РЕАЛЬНАЯ КАРТА DOF ===")

    print(f"Карта элементов: {dof_map}")
    print(f"Количество DOF: {number_of_dofs}")

    assert dof_map == [
        [0, 1, 2, 3],
        [2, 4, 5, 6]
    ]

    assert number_of_dofs == 7

    print("\nПроверки пройдены.")


if __name__ == "__main__":
    test_internal_hinge_dof_mapping_real()