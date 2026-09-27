import numpy as np

from model.beam import Beam
from calculation.influence_response import (
    calculate_reaction_from_unit_load
)


def calculate_influence_line(
    beam: Beam,
    support_position: float,
    number_of_points: int = 101
):
    """
    Строит линию влияния реакции выбранной опоры.

    beam              — исходная расчётная схема.
    support_position  — координата интересующей опоры.
    number_of_points  — количество точек линии влияния.

    Возвращает:
        positions — координаты x.
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

        value = calculate_reaction_from_unit_load(
            beam=beam,
            load_position=float(position),
            support_position=support_position
        )

        values.append(value)

    return positions, np.array(values)