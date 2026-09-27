from calculation.load import create_vertical_nodal_load
from calculation.boundary_conditions import find_node_index

import numpy as np

from model.beam import Beam, SupportType
from calculation.solver import solve_beam
from calculation.section_forces import calculate_moment_at_section
from calculation.boundary_conditions import find_node_index


def test_internal_hinge_current_behavior():

    beam = Beam()

    beam.add_span(6.0)

    beam.add_support(0.0, SupportType.PINNED)
    beam.add_support(6.0, SupportType.ROLLER)

    # Внутренний шарнир в середине балки
    beam.add_internal_hinge(3.0)

    # Для расчёта пока вручную делаем узлы
    calculation_beam = beam.copy()
    calculation_beam.insert_node(3.0)
    calculation_beam.insert_node(1.5)
###############################################################
    load_node = find_node_index(
        calculation_beam,
        1.5
    )

    loads = create_vertical_nodal_load(
        calculation_beam,
        load_node,
        -1.0
    )


###############################################
    displacements = solve_beam(
        calculation_beam,
        loads
    )

    moment = calculate_moment_at_section(
        calculation_beam,
        displacements,
        3.0
    )

    print("\n=== ДИАГНОСТИКА ВНУТРЕННЕГО ШАРНИРА ===")
    print(f"Положение шарнира: x = 3.00 м")
    print(f"Момент в шарнире: M = {moment:.6f}")

    print("\nПролёты расчётной модели:")
    current_position = 0.0

    for i, span in enumerate(calculation_beam.spans, start=1):
        print(
            f"  Элемент {i}: "
            f"{current_position:.2f} — "
            f"{current_position + span.length:.2f} м"
        )
        current_position += span.length

if __name__ == "__main__":
    test_internal_hinge_current_behavior()