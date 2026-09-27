import numpy as np

from model.beam import Beam
from calculation.dof_mapping import (
    get_number_of_dofs,
    get_vertical_dof
)
from calculation.load import create_vertical_nodal_load
from calculation.solver import solve_beam
from calculation.reactions import calculate_reactions


def calculate_reaction_at_support(
    beam: Beam,
    load_position: float,
    support_position: float,
    load_value: float = -1.0
) -> float:
    """
    Рассчитывает реакцию в заданной опоре
    от сосредоточенной вертикальной нагрузки.

    load_position:
        координата нагрузки.

    support_position:
        координата опоры.

    load_value:
        значение нагрузки.
        По умолчанию -1.0 — единичная нагрузка вниз.
    """

    if load_position < 0 or load_position > beam.total_length:
        raise ValueError(
            "Координата нагрузки находится вне балки."
        )

    if support_position < 0 or support_position > beam.total_length:
        raise ValueError(
            "Координата опоры находится вне балки."
        )

    # Добавляем узел только внутри балки.
    # На концах балки узел уже существует.
    if (
            load_position > 0
            and load_position < beam.total_length
    ):
        beam.insert_node(load_position)

    # Находим узел нагрузки.
    load_node = find_node_by_position(
        beam,
        load_position
    )

    loads = create_vertical_nodal_load(
        beam,
        load_node,
        load_value
    )

    displacements = solve_beam(
        beam,
        loads
    )

    reactions = calculate_reactions(
        beam,
        loads,
        displacements
    )

    # Находим вертикальную степень свободы опоры.
    support_node = find_node_by_position(
        beam,
        support_position
    )

    support_dof = get_vertical_dof(
        beam,
        support_node
    )

    return reactions[support_dof]


def find_node_by_position(
    beam: Beam,
    position: float,
    tolerance: float = 1e-9
) -> int:
    """
    Находит индекс узла по координате.
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


def calculate_reaction_influence_line(
    beam: Beam,
    support_position: float,
    load_positions: np.ndarray
) -> np.ndarray:
    """
    Строит линию влияния реакции заданной опоры.

    Для каждой координаты положения единичной нагрузки
    выполняется отдельный расчёт балки.
    """

    load_positions = np.asarray(
        load_positions,
        dtype=float
    )

    influence_values = []

    for load_position in load_positions:

        calculation_beam = beam.copy()

        value = calculate_reaction_at_support(
            calculation_beam,
            load_position,
            support_position
        )

        influence_values.append(value)

    return np.asarray(
        influence_values,
        dtype=float
    )