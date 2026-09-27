from model.beam import Beam, SupportType
from calculation.influence import calculate_influence_line
from calculation.influence_data import prepare_influence_data
from interface.influence_plot import (
    plot_beam_scheme,
    animate_load_position
)
import matplotlib.pyplot as plt


def test_beam_and_influence():

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

    section_position = 3.0

    result = calculate_influence_line(
        beam,
        quantity="M",
        position=section_position,
        number_of_points=21
    )

    data = prepare_influence_data(result)

    load_position = data["positions"][5]

    print(
        f"\nПоложение нагрузки: "
        f"x = {load_position:.2f} м"
    )

    print("\n=== ПОЛОЖЕНИЯ НАГРУЗКИ ===")

    for position in data["positions"][::5]:

        print(
            f"x = {position:.2f} м"
        )

    print("\n=== ДАННЫЕ ЛИНИИ ВЛИЯНИЯ M ===")

    print(data)

    animate_load_position(
        beam,
        data["positions"],
        section_position=section_position,
        values=data["values"]
    )


if __name__ == "__main__":
    test_beam_and_influence()