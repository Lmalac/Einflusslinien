import numpy as np

from model.beam import Beam, SupportType
from calculation.solver import solve_beam
from calculation.reactions import calculate_reactions
from calculation.boundary_conditions import find_node_index
from calculation.section_forces import calculate_moment_at_section
from calculation.influence_shear import (
    calculate_shear_from_unit_load
)


def create_simple_beam():
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

    return beam


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

    return calculation_beam, loads, displacements, reactions


print("\n=== АВТОМАТИЧЕСКАЯ ПРОВЕРКА ===")


# --------------------------------------------------
# 1. Равновесие простой балки
# --------------------------------------------------

beam = create_simple_beam()

calculation_beam, loads, displacements, reactions = (
    solve_unit_load(beam, 3.0)
)

left_reaction = reactions[0]
right_reaction = reactions[4]

assert np.isclose(left_reaction, 0.5)
assert np.isclose(right_reaction, 0.5)

assert np.isclose(
    left_reaction + right_reaction,
    1.0
)

print("✓ Реакции простой балки")


# --------------------------------------------------
# 2. Момент в середине
# --------------------------------------------------

moment = calculate_moment_at_section(
    beam=calculation_beam,
    displacements=displacements,
    position=3.0
)

assert np.isclose(
    moment,
    -1.5
)

print("✓ Момент в середине")


# --------------------------------------------------
# 3. Поперечная сила
# --------------------------------------------------

q_left = calculate_shear_from_unit_load(
    beam=beam,
    load_position=1.0,
    section_position=3.0,
    side="left"
)

q_right = calculate_shear_from_unit_load(
    beam=beam,
    load_position=5.0,
    section_position=3.0,
    side="right"
)

assert np.isclose(
    q_left,
    -1.0 / 6.0
)

assert np.isclose(
    q_right,
    1.0 / 6.0
)

print("✓ Поперечная сила")


# --------------------------------------------------
# 4. Проверка матрицы и перемещений
# --------------------------------------------------

assert np.all(np.isfinite(displacements))

print("✓ Перемещения конечны")


print("\nВСЕ ПРОВЕРКИ ПРОЙДЕНЫ ✓")