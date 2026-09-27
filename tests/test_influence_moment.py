import numpy as np

from model.beam import Beam, SupportType

from calculation.influence_moment import (
    calculate_moment_influence_line
)


def test_moment_influence_line():

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

    positions, values = calculate_moment_influence_line(
        beam=beam,
        section_position=3.0,
        number_of_points=5
    )

    print("\n=== ЛИНИЯ ВЛИЯНИЯ M В СЕЧЕНИИ x=3 ===")

    for x, value in zip(positions, values):
        print(
            f"x = {x:.2f} м: "
            f"M = {value:.6f}"
        )

    expected = np.array([
        0.0,
        -0.75,
        -1.5,
        -0.75,
        0.0
    ])

    assert np.allclose(
        values,
        expected,
        atol=1e-9
    )


if __name__ == "__main__":
    test_moment_influence_line()