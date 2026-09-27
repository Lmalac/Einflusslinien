import numpy as np

from model.beam import Beam
from calculation.dof_mapping import (
    get_vertical_dof,
    get_number_of_dofs
)


def create_nodal_load(
    number_of_dofs: int,
    dof: int,
    value: float
) -> np.ndarray:
    """
    Создаёт вектор узловой нагрузки.
    """

    if dof < 0 or dof >= number_of_dofs:
        raise ValueError(
            "Номер степени свободы находится "
            "вне допустимого диапазона."
        )

    loads = np.zeros(number_of_dofs)
    loads[dof] = value

    return loads


def create_vertical_nodal_load(
    beam: Beam,
    node_index: int,
    value: float
) -> np.ndarray:
    """
    Создаёт вертикальную узловую нагрузку
    по номеру узла.
    """

    number_of_dofs = get_number_of_dofs(beam)

    vertical_dof = get_vertical_dof(
        beam,
        node_index
    )

    return create_nodal_load(
        number_of_dofs=number_of_dofs,
        dof=vertical_dof,
        value=value
    )