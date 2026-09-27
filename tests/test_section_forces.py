import numpy as np

from model.beam import Beam, SupportType
from calculation.solver import solve_beam
from calculation.section_forces import (
    calculate_moment_at_section
)
from calculation.boundary_conditions import find_node_index


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


# Добавляем узел под нагрузкой.
calculation_beam = beam.copy()
calculation_beam.insert_node(3.0)

number_of_nodes = len(calculation_beam.spans) + 1
number_of_dofs = number_of_nodes * 2

loads = np.zeros(number_of_dofs)


# Единичная нагрузка в x = 3 м.
node_index = find_node_index(
    calculation_beam,
    3.0
)

loads[2 * node_index] = -1.0


# Решаем.
displacements = solve_beam(
    calculation_beam,
    loads
)


print("\n=== ПРОВЕРКА МОМЕНТА ===")

for position in [0.0, 1.5, 3.0, 4.5, 6.0]:

    moment = calculate_moment_at_section(
        beam=calculation_beam,
        displacements=displacements,
        position=position
    )

    print(
        f"x = {position:.1f} м → "
        f"M = {moment:.6f}"
    )