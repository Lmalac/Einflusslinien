from model.beam import Beam, SupportType

from calculation.influence import calculate_influence_line
from calculation.influence_data import prepare_influence_data
from interface.influence_plot import plot_influence_line


def test_plot_moment():

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

    result = calculate_influence_line(
        beam=beam,
        quantity="M",
        position=3.0,
        number_of_points=21
    )

    data = prepare_influence_data(result)

    print("\n=== ПОСТРОЕНИЕ ГРАФИКА M ===")
    print(data)

    plot_influence_line(data)


if __name__ == "__main__":
    test_plot_moment()