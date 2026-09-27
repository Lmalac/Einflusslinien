from model.beam import Beam, SupportType
from calculation.influence_moment import (
    calculate_moment_influence_line
)


beam = Beam()

beam.add_span(6.0, 1.0)

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
    number_of_points=13
)


print("\n=== ЛИНИЯ ВЛИЯНИЯ МОМЕНТА ===")

for x, value in zip(positions, values):

    print(
        f"x = {x:.2f} м → "
        f"M = {value:.6f}"
    )