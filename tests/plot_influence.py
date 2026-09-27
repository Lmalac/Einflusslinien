import matplotlib.pyplot as plt

from model.beam import Beam, SupportType
from calculation.influence_line import (
    calculate_influence_line
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


positions, values = calculate_influence_line(
    beam=beam,
    reaction_dof=0,
    number_of_points=101
)


plt.figure(figsize=(10, 5))

plt.plot(
    positions,
    values,
    linewidth=2
)

plt.axhline(
    0,
    linewidth=1
)

plt.xlabel("Координата x, м")
plt.ylabel("Ордината линии влияния")
plt.title("Линия влияния левой реакции R_A")

plt.grid(True)

plt.show()
