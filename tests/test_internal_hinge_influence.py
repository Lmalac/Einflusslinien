from model.beam import Beam, SupportType
from calculation.influence import calculate_influence_line


def create_beam_with_internal_hinge():

    beam = Beam()

    beam.add_span(4.0)
    beam.add_span(4.0)

    beam.add_support(
        0.0,
        SupportType.PINNED
    )

    beam.add_support(
        8.0,
        SupportType.ROLLER
    )

    beam.add_internal_hinge(
        4.0
    )

    return beam


def find_value(
    positions,
    values,
    target
):

    for position, value in zip(
        positions,
        values
    ):

        if abs(position - target) < 1e-9:
            return value

    raise ValueError(
        f"Не найдена точка x = {target}"
    )


def test_internal_hinge_influence():

    beam = create_beam_with_internal_hinge()

    print()
    print("=" * 60)
    print("ТЕСТ ВНУТРЕННЕГО ШАРНИРА")
    print("=" * 60)

    beam.print_scheme()

    control_points = [
        0.0,
        2.0,
        4.0,
        6.0,
        8.0
    ]

    # --------------------------------------------------
    # M в шарнире
    # --------------------------------------------------

    result_m = calculate_influence_line(
        beam,
        quantity="M",
        position=4.0,
        number_of_points=41
    )

    print()
    print("M в внутреннем шарнире x = 4 м:")

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

    # --------------------------------------------------
    # D в шарнире
    # --------------------------------------------------

    result_d = calculate_influence_line(
        beam,
        quantity="D",
        position=4.0,
        number_of_points=41
    )

    print()
    print("D в внутреннем шарнире x = 4 м:")

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

    # --------------------------------------------------
    # R левой опоры
    # --------------------------------------------------

    result_r = calculate_influence_line(
        beam,
        quantity="R",
        position=0.0,
        number_of_points=41
    )

    print()
    print("R левой опоры x = 0 м:")

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
    test_internal_hinge_influence()