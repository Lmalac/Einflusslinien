from model.beam import Beam, SupportType
from calculation.dof_mapping import build_node_dofs


def get_constrained_dofs(beam: Beam) -> list[int]:
    """
    Возвращает список закреплённых степеней свободы.
    """

    constrained_dofs = []

    for support in beam.supports:

        node_index = find_node_index(
            beam,
            support.position
        )

        node_dofs = build_node_dofs(
            beam,
            node_index
        )

        v_dof = node_dofs[0]

        if support.support_type == SupportType.PINNED:
            constrained_dofs.append(v_dof)

        elif support.support_type == SupportType.ROLLER:
            constrained_dofs.append(v_dof)

        elif support.support_type == SupportType.FIXED:
            constrained_dofs.append(v_dof)

            # У обычного узла второй DOF — theta.
            # У шарнирного узла заделка сейчас не поддерживается
            # как специальный случай.
            if len(node_dofs) == 2:
                theta_dof = node_dofs[1]
                constrained_dofs.append(theta_dof)

        elif support.support_type == SupportType.FREE:
            pass

    return sorted(set(constrained_dofs))


def find_node_index(
    beam: Beam,
    position: float,
    tolerance: float = 1e-9
) -> int:
    """
    Находит номер узла по его координате.
    """

    current_position = 0.0

    for node_index in range(len(beam.spans) + 1):

        if abs(current_position - position) < tolerance:
            return node_index

        if node_index < len(beam.spans):
            current_position += beam.spans[node_index].length

    raise ValueError(
        f"Не удалось найти узел в координате x = {position}."
    )