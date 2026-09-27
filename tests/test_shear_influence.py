from model.beam import Beam, SupportType
from calculation.influence_shear import (
    calculate_shear_influence_line
)


beam = Beam()

beam.add_span(6.0, 1.0)

beam.add_support(0.0, SupportType.PINNED)
beam.add_support(6.0, SupportType.ROLLER)


section_position = 3.0


positions_left, values_left = calculate_shear_influence_line(
    beam=beam,
    section_position=section_position,
    number_of_points=13,
    side="left"
)

positions_right, values_right = calculate_shear_influence_line(
    beam=beam,
    section_position=section_position,
    number_of_points=13,
    side="right"
)


print("\n=== ЛИНИЯ ВЛИЯНИЯ Q ===")
print("Однопролётная балка, сечение x = 3 м")

print("\nQ слева от сечения:")

for x, value in zip(positions_left, values_left):
    print(f"x = {x:.2f} м → Q_left = {value:.6f}")


print("\nQ справа от сечения:")

for x, value in zip(positions_right, values_right):
    print(f"x = {x:.2f} м → Q_right = {value:.6f}")