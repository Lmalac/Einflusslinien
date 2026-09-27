import numpy as np

from model.beam import Beam, SupportType
from calculation.solver import solve_beam
from calculation.reactions import calculate_reactions
from calculation.element_forces import calculate_element_forces
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


# Добавляем узел в середине пролёта.
calculation_beam = beam.copy()
calculation_beam.insert_node(3.0)

number_of_nodes = len(calculation_beam.spans) + 1
number_of_dofs = number_of_nodes * 2

loads = np.zeros(number_of_dofs)


# Единичная нагрузка вниз в x = 3 м.
node_index = find_node_index(
    calculation_beam,
    3.0
)

load_dof = 2 * node_index

loads[load_dof] = -1.0


# Решаем систему.
displacements = solve_beam(
    calculation_beam,
    loads
)

# Реакции.
reactions = calculate_reactions(
    calculation_beam,
    loads,
    displacements
)


print("\n=== КОНЦЕВЫЕ УСИЛИЯ ЭЛЕМЕНТОВ ===")

for element_index in range(len(calculation_beam.spans)):

    forces = calculate_element_forces(
        beam=calculation_beam,
        displacements=displacements,
        element_index=element_index,
        loads=loads
    )

    print(
        f"\nЭлемент {element_index + 1}:"
    )

    print(
        f"  V_left  = {forces[0]:.6f}"
    )

    print(
        f"  M_left  = {forces[1]:.6f}"
    )

    print(
        f"  V_right = {forces[2]:.6f}"
    )

    print(
        f"  M_right = {forces[3]:.6f}"
    )


print("\n=== РЕАКЦИИ ===")

for i, reaction in enumerate(reactions):
    print(
        f"DOF {i}: {reaction:.6f}"
    )