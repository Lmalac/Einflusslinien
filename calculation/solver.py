import numpy as np

from model.beam import Beam
from calculation.global_stiffness import build_global_stiffness
from calculation.boundary_conditions import get_constrained_dofs


def solve_beam(
    beam: Beam,
    loads: np.ndarray
) -> np.ndarray:
    """
    Решает систему K * u = F.

    beam  — расчётная схема балки
    loads — вектор внешних нагрузок

    Возвращает:
        u — вектор перемещений и поворотов.

    Если расчётная схема кинематически изменяема,
    возбуждается ValueError.
    """

    K = build_global_stiffness(beam)

    if len(loads) != K.shape[0]:
        raise ValueError(
            "Размер вектора нагрузок не соответствует "
            "количеству степеней свободы."
        )

    constrained = get_constrained_dofs(beam)

    all_dofs = np.arange(K.shape[0])

    free_dofs = np.array(
        [
            dof
            for dof in all_dofs
            if dof not in constrained
        ]
    )

    Kff = K[np.ix_(free_dofs, free_dofs)]

    Ff = loads[free_dofs]

    # Проверяем устойчивость расчётной схемы.
    #
    # Если матрица свободных DOF вырождена или
    # практически вырождена, конструкция имеет
    # кинематическую изменяемость.
    rank = np.linalg.matrix_rank(Kff)

    if rank < Kff.shape[0]:
        raise ValueError(
            "Расчётная схема кинематически изменяема: "
            "матрица жёсткости вырождена."
        )

    u = np.zeros(K.shape[0])

    u[free_dofs] = np.linalg.solve(
        Kff,
        Ff
    )

    return u