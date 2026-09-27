import numpy as np

from model.beam import Beam
from calculation.beam_element import beam_element_stiffness
from calculation.dof_mapping import (
    build_element_dof_map,
    get_number_of_dofs
)


def build_global_stiffness(beam: Beam) -> np.ndarray:
    """
    Формирует глобальную матрицу жёсткости всей балки.

    Для обычного узла:
        v, theta

    Для внутреннего шарнира:
        общий v
        независимые theta слева и справа
    """

    if len(beam.spans) == 0:
        raise ValueError(
            "Балка должна содержать хотя бы один пролёт."
        )

    element_dof_map = build_element_dof_map(beam)

    number_of_dofs = get_number_of_dofs(beam)

    global_matrix = np.zeros(
        (number_of_dofs, number_of_dofs)
    )

    for element_index, span in enumerate(beam.spans):

        element_matrix = beam_element_stiffness(
            length=span.length,
            relative_ei=span.relative_ei
        )

        dof = element_dof_map[element_index]

        for i in range(4):
            for j in range(4):
                global_matrix[dof[i], dof[j]] += (
                    element_matrix[i, j]
                )

    return global_matrix