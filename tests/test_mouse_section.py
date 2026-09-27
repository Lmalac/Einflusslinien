import matplotlib.pyplot as plt

from model.beam import Beam, SupportType
from calculation.influence import calculate_influence_line
from calculation.influence_data import prepare_influence_data
from interface.influence_plot import animate_load_position


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


def select_section(event, beam):

    if event.inaxes is None:
        return

    if event.xdata is None:
        return

    position = event.xdata

    # Проверяем границы балки
    if position < 0:
        position = 0.0

    if position > beam.total_length:
        position = beam.total_length

    print(
        f"\nВыбрано сечение: "
        f"x = {position:.3f} м"
    )

    # Расчёт линии влияния M
    result = calculate_influence_line(
        beam,
        quantity="M",
        position=position,
        number_of_points=41
    )

    data = prepare_influence_data(result)

    # Максимум и минимум
    values = data["values"]

    maximum = max(values)
    minimum = min(values)

    print(
        f"Максимум M = {maximum:.6f}"
    )

    print(
        f"Минимум M = {minimum:.6f}"
    )

    # Запускаем анимацию
    animate_load_position(
        beam,
        data["positions"],
        section_position=position,
        values=data["values"]
    )


def test_mouse_section():

    beam = create_beam()

    fig, ax = plt.subplots(
        figsize=(10, 2)
    )

    # Балка
    ax.plot(
        [0, beam.total_length],
        [0, 0],
        linewidth=4
    )

    # Опоры
    for support in beam.supports:

        x = support.position

        if support.support_type == SupportType.PINNED:

            ax.plot(
                x,
                0,
                marker="^",
                markersize=14
            )

        elif support.support_type == SupportType.ROLLER:

            ax.plot(
                x,
                0,
                marker="o",
                markersize=12
            )

    ax.set_xlim(
        -0.5,
        beam.total_length + 0.5
    )

    ax.set_ylim(
        -1,
        1
    )

    ax.set_xlabel(
        "Координата, м"
    )

    ax.set_yticks([])

    ax.grid(
        True,
        axis="x"
    )

    ax.set_title(
        "Щёлкните мышью по балке"
    )

    fig.canvas.mpl_connect(
        "button_press_event",
        lambda event: select_section(
            event,
            beam
        )
    )

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    test_mouse_section()