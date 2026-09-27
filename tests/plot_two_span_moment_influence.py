import matplotlib.pyplot as plt

from model.beam import Beam, SupportType
from calculation.influence_moment import (
    calculate_moment_influence_line
)


beam = Beam()

beam.add_span(6.0, 1.0)
beam.add_span(6.0, 1.0)

beam.add_support(0.0, SupportType.PINNED)
beam.add_support(6.0, SupportType.ROLLER)
beam.add_support(12.0, SupportType.ROLLER)


positions, values = calculate_moment_influence_line(
    beam=beam,
    section_position=3.0,
    number_of_points=101
)


plt.figure(figsize=(10, 5))

plt.plot(
    positions,
    values,
    linewidth=2
)

plt.axhline(0, linewidth=1)
plt.axvline(
    3.0,
    linewidth=1,
    linestyle="--"
)

plt.xlabel("Положение единичной нагрузки, м")
plt.ylabel("Ордината линии влияния M")
plt.title(
    "Линия влияния изгибающего момента "
    "в сечении x = 3 м"
)

plt.grid(True)
plt.show()