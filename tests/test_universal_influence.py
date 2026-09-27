from model.beam import Beam, SupportType

from calculation.influence import (
    calculate_influence_line
)


def test_universal_influence_invalid_quantity():

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

    try:
        calculate_influence_line(
            beam=beam,
            quantity="N",
            position=3.0,
            number_of_points=5
        )

    except ValueError as error:

        print("\n=== ТЕСТ НЕИЗВЕСТНОЙ ВЕЛИЧИНЫ ===")
        print("ValueError получена корректно:")
        print(error)

        assert "Неизвестная величина" in str(error)
        return

    raise AssertionError(
        "Ожидалась ошибка ValueError, "
        "но расчёт её не вызвал."
    )


if __name__ == "__main__":
    test_universal_influence_invalid_quantity()
    print("ТЕСТ ПРОЙДЕН")