def test_internal_hinge_dof_map():

    print("\n=== КАРТА DOF ВНУТРЕННЕГО ШАРНИРА ===")

    # Балка:
    #
    # A -------- ○ -------- B
    # 0          3          6
    #
    # Шарнир в x = 3 м.
    #
    # Общий вертикальный DOF шарнира:
    #     vH = 2
    #
    # Независимые повороты:
    #     theta_left  = 3
    #     theta_right = 4

    left_element_dofs = [0, 1, 2, 3]
    right_element_dofs = [2, 4, 5, 6]

    print(f"Левый элемент:  {left_element_dofs}")
    print(f"Правый элемент: {right_element_dofs}")

    # Проверяем общий вертикальный DOF шарнира.
    assert left_element_dofs[2] == right_element_dofs[0]
    assert left_element_dofs[2] == 2

    # Проверяем независимые повороты шарнира.
    theta_left = left_element_dofs[3]
    theta_right = right_element_dofs[1]

    assert theta_left == 3
    assert theta_right == 4
    assert theta_left != theta_right

    # Всего должно быть 7 DOF.
    all_dofs = set(
        left_element_dofs + right_element_dofs
    )

    assert all_dofs == {0, 1, 2, 3, 4, 5, 6}

    print("\nПроверки пройдены.")
    print("Общий v шарнира: DOF 2")
    print("Левый поворот:   DOF 3")
    print("Правый поворот:  DOF 4")
    print("Всего DOF:        7")


if __name__ == "__main__":
    test_internal_hinge_dof_map()