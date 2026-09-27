from model.beam import Beam, SupportType


def test_internal_hinge_structure():

    beam = Beam()

    beam.add_span(6.0)

    beam.add_support(0.0, SupportType.PINNED)
    beam.add_support(6.0, SupportType.ROLLER)

    beam.add_internal_hinge(3.0)

    print("\n=== СТРУКТУРА С ВНУТРЕННИМ ШАРНИРОМ ===")

    print(f"Общая длина: {beam.total_length:.2f} м")

    print("\nПролёты:")

    current_position = 0.0

    for i, span in enumerate(beam.spans, start=1):
        print(
            f"  Элемент {i}: "
            f"{current_position:.2f} — "
            f"{current_position + span.length:.2f} м"
        )

        current_position += span.length

    print("\nВнутренние шарниры:")

    for hinge in beam.internal_hinges:
        print(
            f"  x = {hinge.position:.2f} м"
        )
    print(
        "\nШарнир в x=3.0:",
        beam.is_internal_hinge(3.0)
    )

    print(
        "Шарнир в x=2.0:",
        beam.is_internal_hinge(2.0)
    )

if __name__ == "__main__":
    test_internal_hinge_structure()
