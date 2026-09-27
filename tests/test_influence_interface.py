import numpy as np

from model.beam import Beam, SupportType

from calculation.influence import (
    calculate_shear_influence_line
)


def test_shear_influence_interface():

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

    positions, left_values, right_values = (
        calculate_shear_influence_line(
            beam=beam,
            section_position=3.0,
            number_of_points=5
        )
    )

    print("\n=== ЕДИНЫЙ ИНТЕРФЕЙС Q ===")

    for x, q_left, q_right in zip(
        positions,
        left_values,
        right_values
    ):
        print(
            f"x = {x:.2f} м: "
            f"Q_left = {q_left:.6f}, "
            f"Q_right = {q_right:.6f}"
        )

    expected_positions = np.array([
        0.0,
        1.5,
        3.0,
        4.5,
        6.0
    ])

    assert np.allclose(
        positions,
        expected_positions
    )

    assert len(left_values) == 5
    assert len(right_values) == 5


if __name__ == "__main__":
    test_shear_influence_interface()