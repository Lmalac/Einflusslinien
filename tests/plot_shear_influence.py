import matplotlib.pyplot as plt

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
    number_of_points=101,
    side="left"
)

positions_right, values_right = calculate_shear_influence_line(
    beam=beam,
    section_position=section_position,
    number_of_points=101,
    side="right"
)


plt.figure(figsize=(10, 5))

plt.plot(
    positions_left,
    values_left,
    linewidth=2,
    label="Q слева"
)

plt.plot(
    positions_right,
    values_right,
    linewidth=2,
    linestyle="--",
    label="Q справа"
)

plt.axhline(0, linewidth=1)

plt.axvline(
    section_position,
    linewidth=1,
    linestyle=":"
)

plt.xlabel("Положение единичной нагрузки, м")
plt.ylabel("Ордината линии влияния Q")

plt.title(
    "Линия влияния поперечной силы "
    "в сечении x = 3 м"
)

plt.legend()
plt.grid(True)
plt.show()