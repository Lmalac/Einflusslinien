import numpy as np

from model.beam import Beam
from calculation.dof_mapping import (
    build_element_dof_map,
    get_number_of_dofs
)


def calculate_deflection_at_section(
    beam: Beam,
    displacements: np.ndarray,
    position: float
) -> float:

    if position < 0 or position > beam.total_length:

        raise ValueError(
            "Координата сечения находится вне балки."
        )

    number_of_dofs = get_number_of_dofs(
        beam
    )

    if len(displacements) != number_of_dofs:

        raise ValueError(
            "Размер вектора перемещений "
            "не соответствует количеству "
            "степеней свободы."
        )

    element_dof_map = build_element_dof_map(
        beam
    )

    current_position = 0.0
    tolerance = 1e-9

    for element_index, span in enumerate(
        beam.spans
    ):

        start = current_position
        end = current_position + span.length

        if (
            start - tolerance
            <= position
            <= end + tolerance
        ):

            L = span.length

            dof = element_dof_map[
                element_index
            ]

            element_displacements = (
                displacements[dof]
            )

            v1 = element_displacements[0]
            theta1 = element_displacements[1]

            v2 = element_displacements[2]
            theta2 = element_displacements[3]

            x = position - start

            xi = x / L

            N1 = (
                1
                - 3 * xi ** 2
                + 2 * xi ** 3
            )

            N2 = (
                L
                * (
                    xi
                    - 2 * xi ** 2
                    + xi ** 3
                )
            )

            N3 = (
                3 * xi ** 2
                - 2 * xi ** 3
            )

            N4 = (
                L
                * (
                    -xi ** 2
                    + xi ** 3
                )
            )

            deflection = (
                N1 * v1
                + N2 * theta1
                + N3 * v2
                + N4 * theta2
            )

            return deflection

        current_position = end

    raise ValueError(
        f"Не удалось определить элемент "
        f"для x = {position}."
    )