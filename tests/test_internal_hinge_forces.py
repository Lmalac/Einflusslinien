from model.beam import Beam, SupportType
from calculation.load import create_vertical_nodal_load
from calculation.boundary_conditions import find_node_index
from calculation.solver import solve_beam
from calculation.element_forces import calculate_element_forces


def test_internal_hinge_forces():

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

    # Узел приложения нагрузки x = 1.5 м
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

    print("\n=== ПРОВЕРКА СИЛ ВНУТРЕННЕМ ШАРНИРЕ ===")

    for element_index in range(len(beam.spans)):

        forces = calculate_element_forces(
            beam,
            displacements,
            element_index
        )

        print(
            f"\nЭлемент {element_index + 1}:"
        )

        print(
            f"  Левая сторона:  V = {forces[0]:.6f}, "
            f"M = {forces[1]:.6f}"
        )

        print(
            f"  Правая сторона: V = {forces[2]:.6f}, "
            f"M = {forces[3]:.6f}"
        )

    print("\nПроверяем момент в шарнире...")

    left_element_forces = calculate_element_forces(
        beam,
        displacements,
        1
    )

    right_element_forces = calculate_element_forces(
        beam,
        displacements,
        2
    )

    print(
        f"M слева от шарнира = "
        f"{left_element_forces[3]:.6f}"
    )

    print(
        f"M справа от шарнира = "
        f"{right_element_forces[1]:.6f}"
    )


if __name__ == "__main__":
    test_internal_hinge_forces()