from model.beam import Beam, SupportType
from calculation.influence import calculate_influence_line


def create_two_span_beam():

    beam = Beam()

    beam.add_span(4.0)
    beam.add_span(4.0)

    beam.add_support(
        0.0,
        SupportType.PINNED
    )

    beam.add_support(
        4.0,
        SupportType.ROLLER
    )

    beam.add_support(
        8.0,
        SupportType.ROLLER
    )

    return beam


def find_value(positions, values, target):

    for position, value in zip(
        positions,
        values
    ):

        if abs(position - target) < 1e-9:
            return value

    raise ValueError(
        f"Не найдена точка x = {target}"
    )


def test_two_span_control_points():

    beam = create_two_span_beam()

    control_points = [
        0.0,
        2.0,
        4.0,
        6.0,
        8.0
    ]

    print()
    print("=" * 60)
    print("КОНТРОЛЬНЫЕ ТОЧКИ ДВУХПРОЛЁТНОЙ БАЛКИ")
    print("=" * 60)

    # M
    result_m = calculate_influence_line(
        beam,
        quantity="M",
        position=2.0,
        number_of_points=41
    )

    print()
    print("M в сечении x = 2 м:")

    for x in control_points:

        value = find_value(
            result_m["positions"],
            result_m["values"],
            x
        )

        print(
            f"  нагрузка x = {x:.1f} м"
            f" -> M = {value:.6f}"
        )

    # Q
    result_q = calculate_influence_line(
        beam,
        quantity="Q",
        position=2.0,
        number_of_points=41
    )

    print()
    print("Q в сечении x = 2 м:")

    for x in control_points:

        left = find_value(
            result_q["positions"],
            result_q["left_values"],
            x
        )

        right = find_value(
            result_q["positions"],
            result_q["right_values"],
            x
        )

        print(
            f"  нагрузка x = {x:.1f} м"
            f" -> Q_left = {left:.6f}"
            f" | Q_right = {right:.6f}"
        )

    # D
    result_d = calculate_influence_line(
        beam,
        quantity="D",
        position=2.0,
        number_of_points=41
    )

    print()
    print("D в сечении x = 2 м:")

    for x in control_points:

        value = find_value(
            result_d["positions"],
            result_d["values"],
            x
        )

        print(
            f"  нагрузка x = {x:.1f} м"
            f" -> D = {value:.6f}"
        )

    # R
    result_r = calculate_influence_line(
        beam,
        quantity="R",
        position=4.0,
        number_of_points=41
    )

    print()
    print("R промежуточной опоры x = 4 м:")

    for x in control_points:

        value = find_value(
            result_r["positions"],
            result_r["values"],
            x
        )

        print(
            f"  нагрузка x = {x:.1f} м"
            f" -> R = {value:.6f}"
        )

    print()
    print("=" * 60)
    print("ТЕСТ ЗАВЕРШЁН")
    print("=" * 60)


if __name__ == "__main__":
    test_two_span_control_points()