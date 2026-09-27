import numpy as np

from model.beam import Beam
from calculation.beam_element import beam_element_stiffness
from calculation.dof_mapping import (
    build_element_dof_map,
    get_number_of_dofs
)


def calculate_element_forces(
    beam: Beam,
    displacements: np.ndarray,
    element_index: int,
    loads: np.ndarray | None = None
) -> np.ndarray:
    """
    Вычисляет концевые усилия балочного конечного элемента.

    Порядок:
        [V_left, M_left, V_right, M_right]

    element_index — номер элемента, начиная с 0.

    Для внутреннего шарнира повороты слева
    и справа имеют разные DOF.
    """

    number_of_elements = len(beam.spans)

    if element_index < 0 or element_index >= number_of_elements:
        raise ValueError(
            "Номер элемента находится вне допустимого диапазона."
        )

    number_of_dofs = get_number_of_dofs(beam)

    if len(displacements) != number_of_dofs:
        raise ValueError(
            "Размер вектора перемещений не соответствует "
            "количеству степеней свободы."
        )

    if loads is None:
        loads = np.zeros(number_of_dofs)

    if len(loads) != number_of_dofs:
        raise ValueError(
            "Размер вектора нагрузок не соответствует "
            "количеству степеней свободы."
        )

    span = beam.spans[element_index]

    element_matrix = beam_element_stiffness(
        length=span.length,
        relative_ei=span.relative_ei
    )

    # Получаем правильные глобальные DOF элемента.
    #
    # Обычный элемент:
    #     [v1, theta1, v2, theta2]
    #
    # Элемент около внутреннего шарнира:
    #     используются независимые theta
    #     с левой и правой стороны шарнира.
    element_dof_map = build_element_dof_map(beam)

    dof = element_dof_map[element_index]

    element_displacements = displacements[dof]

    # Внутренние концевые усилия элемента:
    #
    # f = k * u
    #
    # Порядок:
    # [V_left, M_left, V_right, M_right]
    element_forces = (
        element_matrix @ element_displacements
    )

    return element_forces