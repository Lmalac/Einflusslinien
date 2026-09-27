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


def find_clicked_support(
    beam,
    position
):

    tolerance = 0.25

    for support in beam.supports:

        if abs(position - support.position) <= tolerance:

            return support

    return None


def calculate_and_show(
    beam,
    quantity,
    position
):

    print()
    print("=" * 40)
    print(
        f"Выбрана величина: {quantity}"
    )
    print(
        f"Положение: x = {position:.3f} м"
    )
    print("=" * 40)

    result = calculate_influence_line(
        beam,
        quantity=quantity,
        position=position,
        number_of_points=41
    )

    data = prepare_influence_data(
        result
    )

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

    elif quantity == "D":

        values = data["values"]

        print()
        print(
            f"Минимум D = "
            f"{min(values):.6f}"
        )

        print(
            f"Максимум D = "
            f"{max(values):.6f}"
        )

        animate_load_position(
            beam,
            data["positions"],
            section_position=position,
            quantity="D",
            values=values
        )


def select_section(
    beam,
    position,
    fig,
    ax
):

    print()
    print("=" * 40)
    print(
        f"Выбрано сечение: x = {position:.3f} м"
    )
    print(
        "Ожидается выбор M, Q или D."
    )
    print("=" * 40)

    button_m_ax = plt.axes(
        [0.25, 0.05, 0.10, 0.08]
    )

    button_q_ax = plt.axes(
        [0.45, 0.05, 0.10, 0.08]
    )

    button_d_ax = plt.axes(
        [0.65, 0.05, 0.10, 0.08]
    )

    from matplotlib.widgets import Button

    btn_m = Button(
        button_m_ax,
        "M"
    )

    btn_q = Button(
        button_q_ax,
        "Q"
    )

    btn_d = Button(
        button_d_ax,
        "D"
    )

    fig.quantity_buttons = (
        button_m_ax,
        button_q_ax,
        button_d_ax,
        btn_m,
        btn_q,
        btn_d
    )

    def close_buttons():

        button_m_ax.set_visible(False)
        button_q_ax.set_visible(False)
        button_d_ax.set_visible(False)

        fig.canvas.draw_idle()

    def on_m(event):

        print()
        print(
            "Нажата кнопка M"
        )

        close_buttons()

        calculate_and_show(
            beam,
            "M",
            position
        )

    def on_q(event):

        print()
        print(
            "Нажата кнопка Q"
        )

        close_buttons()

        calculate_and_show(
            beam,
            "Q",
            position
        )

    def on_d(event):

        print()
        print(
            "Нажата кнопка D"
        )

        close_buttons()

        calculate_and_show(
            beam,
            "D",
            position
        )

    btn_m.on_clicked(
        on_m
    )

    btn_q.on_clicked(
        on_q
    )

    btn_d.on_clicked(
        on_d
    )

    fig.canvas.draw_idle()


def select_support(
    beam,
    support
):

    support_position = support.position

    print()
    print("=" * 40)
    print(
        f"Выбрана опора: "
        f"x = {support_position:.3f} м"
    )
    print(
        f"Тип: "
        f"{support.support_type.value}"
    )
    print("=" * 40)

    result = calculate_influence_line(
        beam,
        quantity="R",
        position=support_position,
        number_of_points=41
    )

    data = prepare_influence_data(
        result
    )

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
        section_position=support_position,
        quantity="R",
        values=values
    )


def on_mouse_click(
    event,
    beam,
    fig,
    ax
):

    if event.inaxes is not ax:
        return

    if event.xdata is None:
        return

    position = event.xdata

    support = find_clicked_support(
        beam,
        position
    )

    if support is not None:

        select_support(
            beam,
            support
        )

        return

    if (
        position < 0
        or position > beam.total_length
    ):

        return

    select_section(
        beam,
        position,
        fig,
        ax
    )


def test_mouse_selection_mq():

    beam = create_beam()

    fig, ax = plt.subplots(
        figsize=(10, 3)
    )

    ax.plot(
        [0, beam.total_length],
        [0, 0],
        linewidth=4
    )

    for support in beam.supports:

        x = support.position

        if support.support_type == SupportType.PINNED:

            ax.plot(
                x,
                0,
                marker="^",
                markersize=16
            )

        elif support.support_type == SupportType.ROLLER:

            ax.plot(
                x,
                0,
                marker="o",
                markersize=14
            )

        elif support.support_type == SupportType.FIXED:

            ax.plot(
                [x, x],
                [-0.3, 0.3],
                linewidth=3
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
        "Кликните по опоре или по сечению балки"
    )

    fig.canvas.mpl_connect(
        "button_press_event",
        lambda event: on_mouse_click(
            event,
            beam,
            fig,
            ax
        )
    )

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    test_mouse_selection_mq()