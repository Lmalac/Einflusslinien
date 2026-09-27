from model.beam import Beam, SupportType
from calculation.load import create_vertical_nodal_load


def test_vertical_load():

    beam = Beam()

    beam.add_span(6.0)

    beam.add_support(0.0, SupportType.PINNED)
    beam.add_support(6.0, SupportType.ROLLER)

    beam.add_internal_hinge(3.0)

    loads = create_vertical_nodal_load(
        beam=beam,
        node_index=1,
        value=-1.0
    )

    print("\n=== ВЕРТИКАЛЬНАЯ НАГРУЗКА ===")
    print(f"Вектор нагрузки: {loads}")

    assert len(loads) == 7
    assert loads[2] == -1.0
    assert sum(abs(loads)) == 1.0

    print("\nПроверки пройдены.")


if __name__ == "__main__":
    test_vertical_load()