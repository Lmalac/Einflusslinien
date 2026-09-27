from model.beam import Beam, SupportType

from calculation.influence import calculate_influence_line


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


def test_influence_deflection():

    beam = create_beam()

    result = calculate_influence_line(
        beam=beam,
        quantity="D",
        position=3.0,
        number_of_points=5
    )

    print()
    print("=" * 50)
    print("ПРОВЕРКА ОБЩЕГО ИНТЕРФЕЙСА — ПРОГИБ D")
    print("=" * 50)

    for position, value in zip(
        result["positions"],
        result["values"]
    ):

        print(
            f"Положение нагрузки: {position:.3f} м"
            f"   D = {value:.6f}"
        )

    print("=" * 50)


if __name__ == "__main__":
    test_influence_deflection()