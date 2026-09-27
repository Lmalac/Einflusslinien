import numpy as np

from model.beam import Beam
from calculation.global_stiffness import build_global_stiffness


def calculate_reactions(
    beam: Beam,
    loads: np.ndarray,
    displacements: np.ndarray
) -> np.ndarray:
    """
    Вычисляет реакции во всех степенях свободы.

    R = K * u - F

    Возвращает полный вектор реакций.
    Для свободных степеней свободы реакции должны быть
    близки к нулю.
    """

    K = build_global_stiffness(beam)

    if len(loads) != K.shape[0]:
        raise ValueError(
            "Размер вектора нагрузок не соответствует "
            "количеству степеней свободы."
        )

    if len(displacements) != K.shape[0]:
        raise ValueError(
            "Размер вектора перемещений не соответствует "
            "количеству степеней свободы."
        )

    reactions = K @ displacements - loads

    return reactions