import numpy as np

from model.beam import Beam, SupportType
from calculation.solver import solve_beam
from calculation.reactions import calculate_reactions


beam = Beam()

beam.add_span(6.0, 1.0)
beam.add_span(6.0, 0.5)

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


# Единичная нагрузка вниз в точке x = 3 м.
calculation_beam = beam.copy()
calculation_beam.insert_node(3.0)

number_of_nodes = len(calculation_beam.spans) + 1
number_of_dofs = number_of_nodes * 2

loads = np.zeros(number_of_dofs)

# Находим узел x = 3 м.
from calculation.boundary_conditions import find_node_index

node_index = find_node_index(
    calculation_beam,
    3.0
)

load_dof = 2 * node_index

loads[load_dof] = -1.0


displacements = solve_beam(
    calculation_beam,
    loads
)

reactions = calculate_reactions(
    calculation_beam,
    loads,
    displacements
)


print("\n=== ПРОВЕРКА РАВНОВЕСИЯ ===")

print("Реакции:")

for i, reaction in enumerate(reactions):
    print(
        f"DOF {i}: {reaction:.6f}"
    )


# Вертикальные реакции находятся
# на DOF 0, 2, 4, 6...
vertical_reactions = reactions[0::2]

sum_reactions = np.sum(vertical_reactions)
sum_loads = np.sum(loads[0::2])

print(
    f"\nСумма вертикальных реакций: "
    f"{sum_reactions:.10f}"
)

print(
    f"Сумма вертикальных нагрузок: "
    f"{sum_loads:.10f}"
)

print(
    f"Сумма сил: "
    f"{sum_reactions + sum_loads:.10f}"
)


assert abs(sum_reactions + sum_loads) < 1e-9

print("\nПРОВЕРКА ПРОЙДЕНА")