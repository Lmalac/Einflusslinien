import numpy as np

from model.beam import Beam, SupportType
from calculation.load import create_vertical_nodal_load
from calculation.solver import solve_beam
from calculation.section_deflection import calculate_deflection_at_section
from calculation.dof_mapping import get_vertical_dof


def create_beam():

    beam = Beam()

    beam.add_span(6.0)

    beam.add_support(
        0.0,
        SupportType.PINNED
    )

    beam.add_support(
        6.0,
        SupportType.ROLLER
    )

    return beam


def test_deflection():

    beam = create_beam()

    # Добавляем узел в середине балки
    beam.insert_node(3.0)

    node_index = 1

    vertical_dof = get_vertical_dof(
        beam,
        node_index
    )

    number_of_dofs = (
        len(beam.spans) + 1
    ) * 2

    loads = np.zeros(
        number_of_dofs
    )

    loads[vertical_dof] = -1.0

    displacements = solve_beam(
        beam,
        loads
    )

    deflection = calculate_deflection_at_section(
        beam,
        displacements,
        3.0
    )

    print()
    print("=" * 40)
    print("ТЕСТ ПРОГИБА")
    print("=" * 40)

    print(
        f"Прогиб в x = 3.000 м: "
        f"{deflection:.6f}"
    )

    print(
        f"Максимальный прогиб: "
        f"{min(displacements[::2]):.6f}"
    )

    print("=" * 40)


if __name__ == "__main__":
    test_deflection()