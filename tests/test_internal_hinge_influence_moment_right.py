import numpy as np

from model.beam import Beam, SupportType

from calculation.influence_moment import (
    calculate_moment_influence_line
)


def test_internal_hinge_moment_influence_right():

    beam = Beam()

    beam.add_span(6.0)

    beam.add_support(
        0.0,
        SupportType.PINNED
    )

    beam.add_support(
        3.0,
        SupportType.ROLLER
    )

    beam.add_support(
        6.0,
        SupportType.ROLLER
    )

    beam.add_internal_hinge(3.0)

    positions, values = calculate_moment_influence_line(
        beam=beam,
        section_position=4.5,
        number_of_points=7
    )

    print("\n=== ЛИНИЯ ВЛИЯНИЯ M В СЕЧЕНИИ x=4.5 ===")

    for x, value in zip(positions, values):
        print(
            f"x = {x:.2f} м: "
            f"M = {value:.6f}"
        )


if __name__ == "__main__":
    test_internal_hinge_moment_influence_right()