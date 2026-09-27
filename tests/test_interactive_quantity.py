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


def calculate_quantity(
    beam,
    quantity,
    position
):

    result = calculate_influence_line(
        beam,
        quantity=quantity,
        position=position,
        number_of_points=41
    )

    return prepare_influence_data(result)


def select_quantity(
    quantity,
    beam,
    position
):

    print()
    print("=" * 40)
    print(f"Выбрана величина: {quantity}")
    print(f"Положение: x = {position:.3f} м")
    print("=" * 40)

    data = calculate_quantity(
        beam,
        quantity,
        position
    )

    print()
    print("Данные расчёта:")
    print(data)

    # ==================================================
    # ИЗГИБАЮЩИЙ МОМЕНТ M
    # ==================================================

    if quantity == "M":

        values = data["values"]

        print()
        print(
            f"Минимум M = "
            f"{min(values):.6f}"
        )

        print(
            f"Максимум M = "
            f"{max(values):.6f}"
        )

        animate_load_position(
            beam,
            data["positions"],
            section_position=position,
            quantity="M",
            values=values
        )

    # ==================================================
    # ПОПЕРЕЧНАЯ СИЛА Q
    # ==================================================

    elif quantity == "Q":

        left_values = data["left_values"]
        right_values = data["right_values"]

        print()
        print(
            f"Минимум Q слева = "
            f"{min(left_values):.6f}"
        )

        print(
            f"Максимум Q слева = "
            f"{max(left_values):.6f}"
        )

        print(
            f"Минимум Q справа = "
            f"{min(right_values):.6f}"
        )

        print(
            f"Максимум Q справа = "
            f"{max(right_values):.6f}"
        )

        animate_load_position(
            beam,
            data["positions"],
            section_position=position,
            quantity="Q",
            left_values=left_values,
            right_values=right_values
        )

    # ==================================================
    # РЕАКЦИЯ R
    # ==================================================

    elif quantity == "R":

        values = data["values"]

        print()
        print(
            f"Минимум R = "
            f"{min(values):.6f}"
        )

        print(
            f"Максимум R = "
            f"{max(values):.6f}"
        )

        animate_load_position(
            beam,
            data["positions"],
            section_position=position,
            quantity="R",
            values=values
        )

    else:

        raise ValueError(
            f"Неизвестная величина: {quantity}"
        )


def test_interactive_quantity():

    beam = create_beam()

    # Сечение для M и Q
    section_position = 3.0

    # Опора для R
    support_position = 0.0

    fig, ax = plt.subplots(
        figsize=(10, 3)
    )

    # ==================================================
    # БАЛКА
    # ==================================================

    ax.plot(
        [0, beam.total_length],
        [0, 0],
        linewidth=4
    )

    # ==================================================
    # ОПОРЫ
    # ==================================================

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

    # ==================================================
    # ВЫБРАННОЕ СЕЧЕНИЕ
    # ==================================================

    ax.axvline(
        section_position,
        linestyle="--",
        linewidth=1
    )

    ax.text(
        section_position,
        0.3,
        f"x = {section_position:.2f} м",
        ha="center"
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
        "Выберите величину: M, Q или R"
    )

    # ==================================================
    # КНОПКИ
    # ==================================================

    button_m = plt.axes(
        [0.25, 0.05, 0.12, 0.08]
    )

    button_q = plt.axes(
        [0.44, 0.05, 0.12, 0.08]
    )

    button_r = plt.axes(
        [0.63, 0.05, 0.12, 0.08]
    )

    from matplotlib.widgets import Button

    btn_m = Button(
        button_m,
        "M"
    )

    btn_q = Button(
        button_q,
        "Q"
    )

    btn_r = Button(
        button_r,
        "R"
    )

    # ==================================================
    # ОБРАБОТЧИК M
    # ==================================================

    def on_m(event):

        select_quantity(
            "M",
            beam,
            section_position
        )

    # ==================================================
    # ОБРАБОТЧИК Q
    # ==================================================

    def on_q(event):

        select_quantity(
            "Q",
            beam,
            section_position
        )

    # ==================================================
    # ОБРАБОТЧИК R
    # ==================================================

    def on_r(event):

        select_quantity(
            "R",
            beam,
            support_position
        )

    btn_m.on_clicked(on_m)
    btn_q.on_clicked(on_q)
    btn_r.on_clicked(on_r)

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    test_interactive_quantity()