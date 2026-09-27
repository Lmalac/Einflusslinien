import numpy as np

from model.beam import Beam, SupportType

from calculation.influence_response import (
    calculate_reaction_influence_line
)


def test_reaction_influence_line():

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

    load_positions = np.array([
        0.0,
        1.5,
        3.0,
        4.5,
        6.0
    ])

    influence = calculate_reaction_influence_line(
        beam,
        support_position=0.0,
        load_positions=load_positions
    )

    print("\n=== ЛИНИЯ ВЛИЯНИЯ РЕАКЦИИ R0 ===")

    for x, value in zip(
        load_positions,
        influence
    ):
        print(
            f"x = {x:.2f} м: "
            f"R0 = {value:.6f}"
        )


if __name__ == "__main__":
    test_reaction_influence_line()