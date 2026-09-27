import numpy as np

from model.beam import Beam, SupportType

from calculation.influence import (
    calculate_influence_line
)

from interface.influence_plot import (
    animate_load_position
)


def create_beam():

    beam = Beam()

    beam.add_span(6.0)

    beam.add_support(
        0.0,
        SupportType.PINNED
    )

    beam.add_support(
        6.0,
        SupportType.ROLLER
    )

    return beam


def test_animation_deflection():

    beam = create_beam()

    result = calculate_influence_line(
        beam=beam,
        quantity="D",
        position=3.0,
        number_of_points=21
    )

    positions = np.asarray(
        result["positions"]
    )

    values = np.asarray(
        result["values"]
    )

    print()
    print("=" * 50)
    print("АНИМАЦИЯ ЛИНИИ ВЛИЯНИЯ ПРОГИБА D")
    print("=" * 50)

    print(
        f"Количество кадров: {len(positions)}"
    )

    print(
        f"Максимальный прогиб: "
        f"{min(values):.6f}"
    )

    print("=" * 50)

    animate_load_position(
        beam=beam,
        positions=positions,
        section_position=3.0,
        values=values,
        quantity="D"
    )


if __name__ == "__main__":
    test_animation_deflection()