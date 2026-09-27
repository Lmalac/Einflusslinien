from model.beam import Beam


def build_element_dof_map(beam: Beam) -> list[list[int]]:
    """
    Обычный узел: [v, theta]
    Внутренний шарнир: [v, theta_left, theta_right]
    """
    element_dof_map = []
    next_dof = 0
    node_dofs = []
    current_position = 0.0

    for node_index in range(len(beam.spans) + 1):
        is_hinge = beam.is_internal_hinge(current_position)

        if is_hinge:
            node_dofs.append([
                next_dof,
                next_dof + 1,
                next_dof + 2
            ])
            next_dof += 3
        else:
            node_dofs.append([
                next_dof,
                next_dof + 1
            ])
            next_dof += 2

        if node_index < len(beam.spans):
            current_position += beam.spans[node_index].length

    for element_index in range(len(beam.spans)):
        left_node = node_dofs[element_index]
        right_node = node_dofs[element_index + 1]

        left_hinge = len(left_node) == 3
        right_hinge = len(right_node) == 3

        left_v = left_node[0]
        right_v = right_node[0]

        if left_hinge:
            left_theta = left_node[2]
        else:
            left_theta = left_node[1]

        if right_hinge:
            right_theta = right_node[1]
        else:
            right_theta = right_node[1]

        element_dof_map.append([
            left_v,
            left_theta,
            right_v,
            right_theta
        ])

    return element_dof_map


def get_number_of_dofs(beam: Beam) -> int:
    dof_map = build_element_dof_map(beam)

    if not dof_map:
        raise ValueError(
            "Балка должна содержать хотя бы один элемент."
        )

    return max(
        max(element_dofs)
        for element_dofs in dof_map
    ) + 1


def get_vertical_dof(
    beam: Beam,
    node_index: int
) -> int:

    current_position = 0.0

    for index in range(len(beam.spans) + 1):

        if index == node_index:
            return build_node_dofs(
                beam,
                node_index
            )[0]

        if index < len(beam.spans):
            current_position += beam.spans[index].length

    raise ValueError(
        f"Не удалось найти узел {node_index}."
    )


def build_node_dofs(
    beam: Beam,
    node_index: int
) -> list[int]:

    current_position = 0.0
    next_dof = 0

    for index in range(len(beam.spans) + 1):

        is_hinge = beam.is_internal_hinge(
            current_position
        )

        if index == node_index:

            if is_hinge:
                return [
                    next_dof,
                    next_dof + 1,
                    next_dof + 2
                ]

            return [
                next_dof,
                next_dof + 1
            ]

        if is_hinge:
            next_dof += 3
        else:
            next_dof += 2

        if index < len(beam.spans):
            current_position += beam.spans[index].length

    raise ValueError(
        f"Не удалось найти узел {node_index}."
    )