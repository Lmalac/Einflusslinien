import numpy as np

from model.beam import Beam
from calculation.beam_element import beam_element_stiffness
from calculation.dof_mapping import (
    build_element_dof_map,
    get_number_of_dofs
)


def calculate_moment_at_section(
    beam: Beam,
    displacements: np.ndarray,
    position: float
) -> float:
    """
    Вычисляет изгибающий момент M
    в заданном сечении балки.

    position — координата сечения вдоль балки.
    """

    if position < 0 or position > beam.total_length:
        raise ValueError(
            "Координата сечения находится вне балки."
        )

    # Внутренний шарнир не передаёт изгибающий момент. Проверяем
    # координату непосредственно до выбора конечного элемента, чтобы
    # результат не зависел от того, какой из соседних элементов найден.
    if beam.is_internal_hinge(position):
        return 0.0

    number_of_dofs = get_number_of_dofs(beam)

    if len(displacements) != number_of_dofs:
        raise ValueError(
            "Размер вектора перемещений не соответствует "
            "количеству степеней свободы."
        )

    element_dof_map = build_element_dof_map(beam)

    current_position = 0.0
    tolerance = 1e-9

    for element_index, span in enumerate(beam.spans):

        start = current_position
        end = current_position + span.length

        if start - tolerance <= position <= end + tolerance:

            L = span.length

            dof = element_dof_map[element_index]

            element_displacements = displacements[dof]

            k = beam_element_stiffness(
                length=L,
                relative_ei=span.relative_ei
            )

            forces = k @ element_displacements

            M_left = forces[1]
            M_right = -forces[3]

            # Внутренний шарнир.
            #
            # В точке шарнира момент должен быть равен нулю.
            if beam.is_internal_hinge(start) and abs(
                position - start
            ) < tolerance:
                return 0.0

            if beam.is_internal_hinge(end) and abs(
                position - end
            ) < tolerance:
                return 0.0

            # Линейная интерполяция момента
            # между левым и правым концами элемента.
            xi = (position - start) / L

            moment = (
                M_left
                + (M_right - M_left) * xi
            )

            return moment

        current_position = end

    raise ValueError(
        f"Не удалось определить элемент для x = {position}."
    )


def calculate_shear_at_section(
    beam: Beam,
    displacements: np.ndarray,
    position: float,
    side: str = "left"
) -> float:
    """
    Вычисляет поперечную силу Q
    в заданном сечении балки.

    side:
        "left"  — непосредственно слева от сечения;
        "right" — непосредственно справа.

    Знак Q определяется текущей системой знаков
    конечного элемента.
    """

    if position < 0 or position > beam.total_length:
        raise ValueError(
            "Координата сечения находится вне балки."
        )

    if side not in ("left", "right"):
        raise ValueError(
            'Параметр side должен быть "left" или "right".'
        )

    number_of_dofs = get_number_of_dofs(beam)

    if len(displacements) != number_of_dofs:
        raise ValueError(
            "Размер вектора перемещений не соответствует "
            "количеству степеней свободы."
        )

    element_dof_map = build_element_dof_map(beam)

    current_position = 0.0
    tolerance = 1e-9

    for element_index, span in enumerate(beam.spans):

        start = current_position
        end = current_position + span.length

        is_left_boundary = (
            abs(position - start) < tolerance
        )

        is_right_boundary = (
            abs(position - end) < tolerance
        )

        if start <= position <= end:

            if not is_left_boundary and not is_right_boundary:

                selected_element = element_index

            elif is_left_boundary and element_index > 0:

                if side == "left":
                    selected_element = element_index - 1
                else:
                    selected_element = element_index

            elif (
                is_right_boundary
                and element_index < len(beam.spans) - 1
            ):

                if side == "left":
                    selected_element = element_index
                else:
                    selected_element = element_index + 1

            else:
                selected_element = element_index

            span_selected = beam.spans[selected_element]

            dof = element_dof_map[selected_element]

            element_displacements = displacements[dof]

            element_matrix = beam_element_stiffness(
                length=span_selected.length,
                relative_ei=span_selected.relative_ei
            )

            forces = (
                element_matrix @ element_displacements
            )

            V_left = forces[0]
            V_right = -forces[2]

            if selected_element == element_index:
                return V_left

            return V_right

        current_position = end

    raise ValueError(
        f"Не удалось определить элемент для x = {position}."
    )
