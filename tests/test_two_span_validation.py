import numpy as np

from model.beam import Beam, SupportType
from calculation.solver import solve_beam
from calculation.reactions import calculate_reactions
from calculation.boundary_conditions import find_node_index


def solve_unit_load(beam, position):

    calculation_beam = beam.copy()

    if (
        position > 0
        and position < calculation_beam.total_length
    ):
        calculation_beam.insert_node(position)

    number_of_nodes = len(calculation_beam.spans) + 1
    number_of_dofs = number_of_nodes * 2

    loads = np.zeros(number_of_dofs)

    node_index = find_node_index(
        calculation_beam,
        position
    )

    loads[2 * node_index] = -1.0

    displacements = solve_beam(
        calculation_beam,
        loads
    )

    reactions = calculate_reactions(
        calculation_beam,
        loads,
        displacements
    )

    return reactions


print("\n=== ПРОВЕРКА ДВУХПРОЛЁТНОЙ БАЛКИ ===")


# --------------------------------------------------
# Балка
# --------------------------------------------------

beam = Beam()

beam.add_span(6.0, 1.0)
beam.add_span(6.0, 0.5)

beam.add_support(0.0, SupportType.PINNED)
beam.add_support(6.0, SupportType.ROLLER)
beam.add_support(12.0, SupportType.ROLLER)


# --------------------------------------------------
# Единичная нагрузка x = 3 м
# --------------------------------------------------

reactions = solve_unit_load(
    beam,
    3.0
)


print("\nРеакции:")

for dof, value in enumerate(reactions):
    print(
        f"DOF {dof}: {value:.6f}"
    )


# --------------------------------------------------
# Проверка вертикального равновесия
# --------------------------------------------------
vertical_reactions = (
    reactions[0]
    + reactions[4]
    + reactions[6]
)



print(
    f"\nСумма вертикальных реакций: "
    f"{vertical_reactions:.10f}"
)

assert np.isclose(
    vertical_reactions,
    1.0
)


# --------------------------------------------------
# Проверка распределения реакций
# --------------------------------------------------

assert np.isclose(
    reactions[0],
    0.4375
)

assert np.isclose(
    reactions[4],
    0.625
)

assert np.isclose(
    reactions[6],
    -0.0625
)

# --------------------------------------------------
# Проверка конечности решения
# --------------------------------------------------

assert np.all(
    np.isfinite(reactions)
)


print("\n✓ Равновесие выполнено")
print("✓ Реакции соответствуют расчёту")
print("✓ Все значения конечны")

print("\nПРОВЕРКА ДВУХПРОЛЁТНОЙ БАЛКИ ПРОЙДЕНА ✓")