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

    data = calculate_quantity(
        beam,
        "R",
        support_position
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


def select_section(
    beam,
    section_position
):

    print()
    print("=" * 40)
    print(
        f"Выбрано сечение: "
        f"x = {section_position:.3f} м"
    )
    print("=" * 40)

    # Пока автоматически запускаем M.
    # Позже здесь сделаем меню M / Q.

    data = calculate_quantity(
        beam,
        "M",
        section_position
    )

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
        section_position=section_position,
        quantity="M",
        values=values
    )


def on_mouse_click(
    event,
    beam
):

    if event.inaxes is None:
        return

    if event.xdata is None:
        return

    position = event.xdata

    # Проверяем, не попали ли в опору
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

    # Проверяем границы балки
    if (
        position < 0
        or position > beam.total_length
    ):

        return

    # Если это не опора — считаем,
    # что выбрано сечение
    select_section(
        beam,
        position
    )


def test_mouse_selection():

    beam = create_beam()

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

    # ==================================================
    # НАСТРОЙКИ
    # ==================================================

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

    # ==================================================
    # ОБРАБОТЧИК
    # ==================================================

    fig.canvas.mpl_connect(
        "button_press_event",
        lambda event: on_mouse_click(
            event,
            beam
        )
    )

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    test_mouse_selection()