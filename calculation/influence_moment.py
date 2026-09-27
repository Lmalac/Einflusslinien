import numpy as np

from model.beam import Beam
from calculation.solver import solve_beam
from calculation.section_forces import (
    calculate_moment_at_section
)
from calculation.boundary_conditions import find_node_index
from calculation.dof_mapping import (
    get_number_of_dofs,
    get_vertical_dof
)
from calculation.load import create_vertical_nodal_load


def calculate_moment_from_unit_load(
    beam: Beam,
    load_position: float,
    section_position: float
) -> float:
    """
    Вычисляет изгибающий момент в заданном сечении
    от единичной нагрузки, перемещаемой по балке.

    load_position:
        положение единичной нагрузки.

    section_position:
        координата интересующего сечения.

    Единичная нагрузка направлена вниз:
        P = -1
    """

    if load_position < 0 or load_position > beam.total_length:
        raise ValueError(
            "Координата нагрузки находится вне балки."
        )

    if section_position < 0 or section_position > beam.total_length:
        raise ValueError(
            "Координата сечения находится вне балки."
        )

    calculation_beam = beam.copy()

    # Добавляем узел под нагрузкой,
    # если нагрузка находится внутри балки.
    if (
        load_position > 0
        and load_position < calculation_beam.total_length
    ):
        calculation_beam.insert_node(load_position)

    # Добавляем узел в интересующем сечении,
    # если сечение находится внутри балки.
    if (
        section_position > 0
        and section_position < calculation_beam.total_length
    ):
        calculation_beam.insert_node(section_position)

    # Находим узел нагрузки.
    load_node_index = find_node_index(
        calculation_beam,
        load_position
    )

    # Вертикальная степень свободы определяется
    # через общий DOF mapping.
    load_dof = get_vertical_dof(
        calculation_beam,
        load_node_index
    )

    number_of_dofs = get_number_of_dofs(
        calculation_beam
    )

    # Формируем вектор нагрузки.
    loads = create_vertical_nodal_load(
        calculation_beam,
        load_node_index,
        -1.0
    )

    # Дополнительная проверка размера.
    if len(loads) != number_of_dofs:
        raise ValueError(
            "Размер вектора нагрузок не соответствует "
            "количеству степеней свободы."
        )

    # Решаем систему.
    displacements = solve_beam(
        calculation_beam,
        loads
    )

    # Вычисляем момент в сечении.
    moment = calculate_moment_at_section(
        beam=calculation_beam,
        displacements=displacements,
        position=section_position
    )

    return moment


def calculate_moment_influence_line(
    beam: Beam,
    section_position: float,
    number_of_points: int = 101
):
    """
    Строит линию влияния изгибающего момента
    в заданном сечении.

    Возвращает:
        positions — положения единичной нагрузки.
        values    — ординаты линии влияния.
    """

    if number_of_points < 2:
        raise ValueError(
            "Количество точек должно быть не меньше 2."
        )

    positions = np.linspace(
        0.0,
        beam.total_length,
        number_of_points
    )

    values = []

    for position in positions:

        value = calculate_moment_from_unit_load(
            beam=beam,
            load_position=float(position),
            section_position=section_position
        )

        values.append(value)

    return positions, np.array(values)