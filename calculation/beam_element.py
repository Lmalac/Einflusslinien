import numpy as np


def beam_element_stiffness(
    length: float,
    relative_ei: float = 1.0
) -> np.ndarray:
    """
    Возвращает локальную матрицу жёсткости
    балочного конечного элемента Эйлера–Бернулли.

    length      — длина элемента
    relative_ei — относительная жёсткость EI / EI0
    """

    if length <= 0:
        raise ValueError("Длина элемента должна быть больше нуля.")

    if relative_ei <= 0:
        raise ValueError("Относительная жёсткость должна быть больше нуля.")

    L = length
    EI = relative_ei

    L2 = L ** 2
    L3 = L ** 3

    k = EI / L3

    matrix = k * np.array([
        [12,       6 * L,   -12,       6 * L],
        [6 * L,    4 * L2,  -6 * L,    2 * L2],
        [-12,     -6 * L,    12,      -6 * L],
        [6 * L,    2 * L2,  -6 * L,    4 * L2]
    ])

    return matrix