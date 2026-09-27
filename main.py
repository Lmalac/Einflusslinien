from model.beam import Beam, SupportType
from calculation.influence_line import calculate_influence_line


beam = Beam()

# Два пролёта по 6 метров
beam.add_span(6.0, 1.0)
beam.add_span(6.0, 0.5)


# Опоры
beam.add_support(
    0.0,
    SupportType.PINNED
)

beam.add_support(
    6.0,
    SupportType.ROLLER
)

beam.add_support(
    12.0,
    SupportType.ROLLER
)

beam.print_scheme()


print("\nЛиния влияния реакции средней опоры B:")

positions, values = calculate_influence_line(
    beam=beam,
    support_position=6.0,
    number_of_points=13
)

for x, value in zip(positions, values):
    print(
        f"x = {x:.2f} м → R_B = {value:.4f}"
    )