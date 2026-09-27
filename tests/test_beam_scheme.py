from model.beam import Beam, SupportType
from interface.influence_plot import plot_beam_scheme
import matplotlib.pyplot as plt


def test_beam_scheme():

    beam = Beam()

    beam.add_span(6.0)
    beam.add_internal_hinge(3.0)

    beam.add_support(
        0.0,
        SupportType.PINNED
    )

    beam.add_support(
        6.0,
        SupportType.ROLLER
    )

    print("\n=== РАСЧЁТНАЯ СХЕМА ===")

    fig, ax = plot_beam_scheme(
        beam,
        section_position=3.0,
        load_position=1.5
    )

    print("Схема построена.")
    print("Закрытие окна завершит тест.")

    plt.show()


if __name__ == "__main__":
    test_beam_scheme()