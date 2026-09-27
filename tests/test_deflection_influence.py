from model.beam import Beam, SupportType

from calculation.influence_deflection import (
    calculate_deflection_influence_line
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


def test_deflection_influence():

    beam = create_beam()

    positions, values = calculate_deflection_influence_line(
        beam=beam,
        section_position=3.0,
        number_of_points=5
    )

    print()
    print("=" * 50)
    print("ЛИНИЯ ВЛИЯНИЯ ПРОГИБА")
    print("=" * 50)

    for position, value in zip(positions, values):

        print(
            f"Положение нагрузки: {position:.3f} м"
            f"   Прогиб: {value:.6f}"
        )

    print("=" * 50)


if __name__ == "__main__":
    test_deflection_influence()