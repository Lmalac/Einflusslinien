from model.beam import Beam, SupportType

from calculation.influence import calculate_influence_line


def create_beam():

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

    beam.add_internal_hinge(
        4.0
    )

    return beam


def test_supported_internal_hinge():

    beam = create_beam()

    print()
    print("=" * 60)
    print("ТЕСТ ВНУТРЕННЕГО ШАРНИРА С ОПОРОЙ")
    print("=" * 60)

    beam.print_scheme()

    # --------------------------------------------------
    # M в шарнире
    # --------------------------------------------------

    print()
    print("M в шарнире x = 4 м:")

    result_m = calculate_influence_line(
        beam,
        quantity="M",
        position=4.0,
        number_of_points=41
    )

    print(
        f"Минимум M = "
        f"{min(result_m['values']):.6f}"
    )

    print(
        f"Максимум M = "
        f"{max(result_m['values']):.6f}"
    )

    # --------------------------------------------------
    # D в шарнире
    # --------------------------------------------------

    print()
    print("D в шарнире x = 4 м:")

    result_d = calculate_influence_line(
        beam,
        quantity="D",
        position=4.0,
        number_of_points=41
    )

    print(
        f"Минимум D = "
        f"{min(result_d['values']):.6f}"
    )

    print(
        f"Максимум D = "
        f"{max(result_d['values']):.6f}"
    )

    # --------------------------------------------------
    # R промежуточной опоры
    # --------------------------------------------------

    print()
    print("R промежуточной опоры x = 4 м:")

    result_r = calculate_influence_line(
        beam,
        quantity="R",
        position=4.0,
        number_of_points=41
    )

    print(
        f"Минимум R = "
        f"{min(result_r['values']):.6f}"
    )

    print(
        f"Максимум R = "
        f"{max(result_r['values']):.6f}"
    )

    print()
    print("=" * 60)
    print("ТЕСТ ЗАВЕРШЁН")
    print("=" * 60)


if __name__ == "__main__":
    test_supported_internal_hinge()