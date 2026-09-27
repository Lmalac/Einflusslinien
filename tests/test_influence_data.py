import numpy as np

from model.beam import Beam, SupportType

from calculation.influence import calculate_influence_line
from calculation.influence_data import prepare_influence_data


def test_real_shear_data():

    beam = Beam()

    beam.add_span(6.0)

    beam.add_support(0.0, SupportType.PINNED)
    beam.add_support(6.0, SupportType.ROLLER)

    result = calculate_influence_line(
        beam=beam,
        quantity="Q",
        position=3.0,
        number_of_points=5
    )

    data = prepare_influence_data(result)

    print("\n=== ПОЛНАЯ ЦЕПОЧКА Q ===")

    print("Результат расчёта:")
    print(result)

    print("\nДанные для интерфейса:")
    print(data)

    assert data["quantity"] == "Q"

    assert data["positions"] == [
        0.0,
        1.5,
        3.0,
        4.5,
        6.0
    ]

    expected_left = [
        0.0,
        -0.25,
        0.5,
        0.25,
        0.0
    ]

    expected_right = [
        0.0,
        -0.25,
        -0.5,
        0.25,
        0.0
    ]

    assert np.allclose(
        data["left_values"],
        expected_left
    )

    assert np.allclose(
        data["right_values"],
        expected_right
    )


if __name__ == "__main__":
    test_real_shear_data()
    print("\nТЕСТ ПРОЙДЕН")