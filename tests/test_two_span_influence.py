from model.beam import Beam, SupportType
from calculation.influence import calculate_influence_line


def create_two_span_beam():

    beam = Beam()

    # Два пролёта по 4 м
    beam.add_span(4.0)
    beam.add_span(4.0)

    # Левая опора
    beam.add_support(
        0.0,
        SupportType.PINNED
    )

    # Промежуточная опора
    beam.add_support(
        4.0,
        SupportType.ROLLER
    )

    # Правая опора
    beam.add_support(
        8.0,
        SupportType.ROLLER
    )

    return beam


def test_two_span_influence():

    beam = create_two_span_beam()

    print()
    print("=" * 50)
    print("ТЕСТ ДВУХПРОЛЁТНОЙ БАЛКИ")
    print("=" * 50)

    beam.print_scheme()

    print()
    print("--- M в x = 2 м ---")

    result_m = calculate_influence_line(
        beam,
        quantity="M",
        position=2.0,
        number_of_points=21
    )

    print(
        f"M: {len(result_m['positions'])} точек"
    )

    print(
        f"M min = {min(result_m['values']):.6f}"
    )

    print(
        f"M max = {max(result_m['values']):.6f}"
    )

    print()
    print("--- Q в x = 2 м ---")

    result_q = calculate_influence_line(
        beam,
        quantity="Q",
        position=2.0,
        number_of_points=21
    )

    print(
        f"Q слева min = "
        f"{min(result_q['left_values']):.6f}"
    )

    print(
        f"Q слева max = "
        f"{max(result_q['left_values']):.6f}"
    )

    print(
        f"Q справа min = "
        f"{min(result_q['right_values']):.6f}"
    )

    print(
        f"Q справа max = "
        f"{max(result_q['right_values']):.6f}"
    )

    print()
    print("--- D в x = 2 м ---")

    result_d = calculate_influence_line(
        beam,
        quantity="D",
        position=2.0,
        number_of_points=21
    )

    print(
        f"D min = {min(result_d['values']):.6f}"
    )

    print(
        f"D max = {max(result_d['values']):.6f}"
    )

    print()
    print("--- R в x = 4 м ---")

    result_r = calculate_influence_line(
        beam,
        quantity="R",
        position=4.0,
        number_of_points=21
    )

    print(
        f"R min = {min(result_r['values']):.6f}"
    )

    print(
        f"R max = {max(result_r['values']):.6f}"
    )

    print()
    print("=" * 50)
    print("ТЕСТ ЗАВЕРШЁН")
    print("=" * 50)


if __name__ == "__main__":
    test_two_span_influence()