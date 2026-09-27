from model.beam import Beam, SupportType
from calculation.influence import calculate_influence_line
from calculation.influence_data import prepare_influence_data


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


def test_quantity_selection():

    beam = create_beam()

    position = 3.0

    print("\n=== M ===")

    result_m = calculate_influence_line(
        beam,
        quantity="M",
        position=position,
        number_of_points=5
    )

    data_m = prepare_influence_data(result_m)

    print(data_m)

    print("\n=== Q ===")

    result_q = calculate_influence_line(
        beam,
        quantity="Q",
        position=position,
        number_of_points=5
    )

    data_q = prepare_influence_data(result_q)

    print(data_q)

    print("\n=== R ===")

    result_r = calculate_influence_line(
        beam,
        quantity="R",
        position=0.0,
        number_of_points=5
    )

    data_r = prepare_influence_data(result_r)

    print(data_r)

    print("\nТЕСТ ПЕРЕКЛЮЧЕНИЯ M / Q / R ПРОЙДЕН")


if __name__ == "__main__":
    test_quantity_selection()