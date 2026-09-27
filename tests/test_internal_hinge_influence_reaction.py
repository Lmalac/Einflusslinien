import numpy as np

from model.beam import Beam, SupportType

from calculation.influence_response import (
    calculate_reaction_influence_line
)


def test_internal_hinge_reaction_influence():

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

    load_positions = np.array([
        0.5,
        1.5,
        2.5,
        3.5,
        4.5,
        5.5
    ])

    influence = calculate_reaction_influence_line(
        beam,
        support_position=3.0,
        load_positions=load_positions
    )

    print("\n=== ЛИНИЯ ВЛИЯНИЯ R3 ===")

    for x, value in zip(
        load_positions,
        influence
    ):
        print(
            f"x = {x:.2f} м: "
            f"R3 = {value:.6f}"
        )


if __name__ == "__main__":
    test_internal_hinge_reaction_influence()