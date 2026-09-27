import numpy as np

from model.beam import Beam, SupportType
from calculation.solver import solve_beam
from calculation.section_forces import (
    calculate_shear_at_section
)
from calculation.boundary_conditions import find_node_index


beam = Beam()

beam.add_span(6.0, 1.0)

beam.add_support(0.0, SupportType.PINNED)
beam.add_support(6.0, SupportType.ROLLER)


calculation_beam = beam.copy()

# Ставим узел в месте действия единичной нагрузки.
calculation_beam.insert_node(3.0)

number_of_nodes = len(calculation_beam.spans) + 1
number_of_dofs = number_of_nodes * 2

loads = np.zeros(number_of_dofs)

node_index = find_node_index(
    calculation_beam,
    3.0
)

loads[2 * node_index] = -1.0

displacements = solve_beam(
    calculation_beam,
    loads
)


print("\n=== ПРОВЕРКА ПОПЕРЕЧНОЙ СИЛЫ ===")

for position in [1.5, 2.9, 3.0, 3.1, 4.5]:

    q_left = calculate_shear_at_section(
        beam=calculation_beam,
        displacements=displacements,
        position=position,
        side="left"
    )

    q_right = calculate_shear_at_section(
        beam=calculation_beam,
        displacements=displacements,
        position=position,
        side="right"
    )

    print(
        f"x = {position:.1f} м → "
        f"Q_left = {q_left:.6f}, "
        f"Q_right = {q_right:.6f}"
    )