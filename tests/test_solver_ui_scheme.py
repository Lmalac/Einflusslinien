from model.beam import Beam, SupportType
from calculation.load import create_vertical_nodal_load
from calculation.solver import solve_beam
from calculation.dof_mapping import get_number_of_dofs

from calculation.reactions import calculate_reactions
from calculation.boundary_conditions import find_node_index
from calculation.dof_mapping import get_vertical_dof

from calculation.section_forces import (
    calculate_moment_at_section,
    calculate_shear_at_section
)
import numpy as np

beam = Beam()

beam.add_span(6.0)
beam.insert_node(3.0)

beam.add_support(
    0.0,
    SupportType.PINNED
)

beam.add_support(
    6.0,
    SupportType.ROLLER
)

number_of_dofs = get_number_of_dofs(beam)

loads = create_vertical_nodal_load(
    beam,
    node_index=1,
    value=-1.0
)

displacements = solve_beam(
    beam,
    loads
)

moment = calculate_moment_at_section(
    beam,
    displacements,
    3.0
)

print("\nИзгибающий момент:")
print(f"M в x = 3 м: {moment:.6f}")

if not np.isclose(
    moment,
    -1.5
):
    raise AssertionError(
        f"Ожидалось M = -1.5, получено {moment}"
    )

print("\nПроверка изгибающего момента пройдена.")

####################################################################
shear_left = calculate_shear_at_section(
    beam,
    displacements,
    3.0,
    side="left"
)

shear_right = calculate_shear_at_section(
    beam,
    displacements,
    3.0,
    side="right"
)

print("\nПоперечная сила:")
print(f"Q слева от x = 3 м: {shear_left:.6f}")
print(f"Q справа от x = 3 м: {shear_right:.6f}")

if not np.isclose(
    shear_left,
    0.5
):
    raise AssertionError(
        f"Ожидалось Q слева = 0.5, получено {shear_left}"
    )

if not np.isclose(
    shear_right,
    -0.5
):
    raise AssertionError(
        f"Ожидалось Q справа = -0.5, получено {shear_right}"
    )

print("\nПроверка поперечной силы пройдена.")





reactions = calculate_reactions(
    beam,
    loads,
    displacements
)

left_node = find_node_index(
    beam,
    0.0
)

right_node = find_node_index(
    beam,
    6.0
)

left_dof = get_vertical_dof(
    beam,
    left_node
)

right_dof = get_vertical_dof(
    beam,
    right_node
)

print("\nРеакции опор:")
print(
    f"Левая опора: {reactions[left_dof]:.6f}"
)

print(
    f"Правая опора: {reactions[right_dof]:.6f}"
)

if not np.isclose(
    reactions[left_dof],
    0.5
) or not np.isclose(
    reactions[right_dof],
    0.5
):
    raise AssertionError(
        "Реакции опор не равны 0.5 и 0.5."
    )

print("\nПроверка реакций опор пройдена.")


from calculation.global_stiffness import build_global_stiffness

K = build_global_stiffness(beam)

calculated_loads = K @ displacements

print("\nK*u:")
print(calculated_loads)

print("\nОшибка K*u - F:")
print(calculated_loads - loads)



from calculation.boundary_conditions import get_constrained_dofs

constrained_dofs = get_constrained_dofs(
    beam
)

free_dofs = [
    dof
    for dof in range(number_of_dofs)
    if dof not in constrained_dofs
]

if not np.allclose(
    calculated_loads[free_dofs],
    loads[free_dofs]
):
    raise AssertionError(
        "Проверка K*u = F на свободных степенях свободы не пройдена."
    )

print(
    "\nПроверка K*u = F "
    "на свободных степенях свободы пройдена."
)




from calculation.global_stiffness import build_global_stiffness

K = build_global_stiffness(beam)

calculated_loads = K @ displacements

print("\nK*u:")
print(calculated_loads)

print("\nОшибка K*u - F:")
print(calculated_loads - loads)



print("=" * 50)
print("ТЕСТ РЕШЕНИЯ K*u=F")
print("=" * 50)

print(f"Количество степеней свободы: {number_of_dofs}")

print("\nВектор F:")
print(loads)

print("\nВектор перемещений u:")
print(displacements)

print("\nПроверка K*u = F:")
print("Расчёт выполнен успешно.")

print("=" * 50)