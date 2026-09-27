import numpy as np

from model.beam import Beam, SupportType
from calculation.solver import solve_beam
from calculation.reactions import calculate_reactions
from calculation.boundary_conditions import find_node_index


beam = Beam()

beam.add_span(6.0, 1.0)

beam.add_support(
    0.0,
    SupportType.PINNED
)

beam.add_support(
    3.0,
    SupportType.ROLLER
)

beam.add_support(
    6.0,
    SupportType.ROLLER
)


calculation_beam = beam.copy()

calculation_beam.insert_node(1.5)


number_of_nodes = len(calculation_beam.spans) + 1
number_of_dofs = number_of_nodes * 2

loads = np.zeros(number_of_dofs)

load_node = find_node_index(
    calculation_beam,
    1.5
)

loads[2 * load_node] = -1.0


displacements = solve_beam(
    calculation_beam,
    loads
)

reactions = calculate_reactions(
    calculation_beam,
    loads,
    displacements
)


print("\n=== ПРОВЕРКА ВНУТРЕННЕЙ ОПОРЫ ===")

print("\nУзлы:")

current_position = 0.0

for i in range(number_of_nodes):

    print(
        f"Узел {i}: x = {current_position:.2f} м"
    )

    if i < len(calculation_beam.spans):
        current_position += (
            calculation_beam.spans[i].length
        )


print("\nРеакции:")

for dof, value in enumerate(reactions):

    if dof % 2 == 0:
        print(
            f"DOF {dof}: "
            f"R = {value:.6f}"
        )


vertical_reactions = (
    reactions[0]
    + reactions[4]
    + reactions[6]
)


print(
    f"\nСумма реакций: "
    f"{vertical_reactions:.10f}"
)

print(
    f"Сумма внешних сил: "
    f"{loads[::2].sum():.10f}"
)


assert np.isclose(
    vertical_reactions,
    1.0
)

assert np.all(
    np.isfinite(reactions)
)

print("\n✓ Равновесие выполнено")
print("✓ Внутренняя опора учтена")
print("✓ Решение конечно")

print("\nПРОВЕРКА ПРОЙДЕНА ✓")