import matplotlib.pyplot as plt

from model.beam import SupportType


def plot_beam_scheme(
    beam,
    section_position=None,
    load_position=None
):
    """
    Рисует расчётную схему балки.
    """

    fig, ax = plt.subplots(figsize=(10, 2))

    total_length = beam.total_length

    # Балка
    ax.plot(
        [0, total_length],
        [0, 0],
        linewidth=3
    )

    # Опоры
    for support in beam.supports:

        x = support.position

        if support.support_type == SupportType.PINNED:

            ax.plot(
                x,
                0,
                marker="^",
                markersize=12
            )

        elif support.support_type == SupportType.ROLLER:

            ax.plot(
                x,
                0,
                marker="o",
                markersize=10
            )

        elif support.support_type == SupportType.FIXED:

            ax.plot(
                [x, x],
                [-0.3, 0.3],
                linewidth=3
            )

    # Внутренние шарниры
    for hinge in beam.internal_hinges:

        x = hinge.position

        ax.plot(
            x,
            0,
            marker="o",
            markersize=8,
            markerfacecolor="white"
        )

        ax.text(
            x,
            -0.35,
            "шарнир",
            ha="center"
        )

    # Единичная нагрузка
    if load_position is not None:

        ax.arrow(
            load_position,
            0.8,
            0,
            -0.6,
            head_width=0.12,
            head_length=0.15,
            length_includes_head=True
        )

        ax.text(
            load_position,
            0.9,
            "P = 1",
            ha="center"
        )

    # Сечение
    if section_position is not None:

        ax.axvline(
            section_position,
            linestyle="--",
            linewidth=1
        )

        ax.text(
            section_position,
            0.35,
            f"x = {section_position:.2f} м",
            ha="center"
        )

    ax.set_xlim(
        -0.5,
        total_length + 0.5
    )

    ax.set_ylim(
        -0.6,
        1.1
    )

    ax.set_xlabel(
        "Координата, м"
    )

    ax.set_yticks([])

    ax.grid(
        True,
        axis="x"
    )

    plt.tight_layout()

    return fig, ax


def plot_influence_line(data: dict):
    """
    Строит линию влияния.
    """

    quantity = data["quantity"]
    positions = data["positions"]

    plt.figure(figsize=(10, 5))

    if quantity in ("M", "R", "D"):

        values = data["values"]

        plt.plot(
            positions,
            values,
            marker="o"
        )

    elif quantity == "Q":

        left_values = data["left_values"]
        right_values = data["right_values"]

        plt.plot(
            positions,
            left_values,
            marker="o",
            label="Q слева"
        )

        plt.plot(
            positions,
            right_values,
            marker="o",
            label="Q справа"
        )

        plt.legend()

    else:

        raise ValueError(
            f"Неизвестная величина: {quantity}"
        )

    plt.axhline(
        0,
        linewidth=0.8
    )

    plt.xlabel(
        "Положение единичной нагрузки, м"
    )

    if quantity == "M":

        plt.ylabel("M")

        plt.title(
            "Линия влияния изгибающего момента M"
        )

    elif quantity == "Q":

        plt.ylabel("Q")

        plt.title(
            "Линия влияния поперечной силы Q"
        )

    elif quantity == "R":

        plt.ylabel("R")

        plt.title(
            "Линия влияния реакции R"
        )

    elif quantity == "D":

        plt.ylabel("D")

        plt.title(
            "Линия влияния прогиба D"
        )

    plt.grid(True)

    plt.tight_layout()

    plt.show()


def animate_load_position(
    beam,
    positions,
    section_position=None,
    values=None,
    quantity="M",
    left_values=None,
    right_values=None
):
    """
    Анимирует перемещение единичной нагрузки.

    Поддерживает:
        M — изгибающий момент;
        Q — поперечную силу;
        R — реакцию опоры;
        D — прогиб.

    Для Q:
        left_values  — значения слева от сечения;
        right_values — значения справа от сечения.

    Для M, R и D:
        values — значения величины.
    """

    from matplotlib.animation import FuncAnimation

    fig, (ax_beam, ax_influence) = plt.subplots(
        2,
        1,
        figsize=(10, 6)
    )

    total_length = beam.total_length

    quantity = quantity.upper()

    # ==================================================
    # ВЕРХНИЙ ГРАФИК — БАЛКА
    # ==================================================

    ax_beam.plot(
        [0, total_length],
        [0, 0],
        linewidth=3
    )

    # Опоры
    for support in beam.supports:

        x = support.position

        if support.support_type == SupportType.PINNED:

            ax_beam.plot(
                x,
                0,
                marker="^",
                markersize=12
            )

        elif support.support_type == SupportType.ROLLER:

            ax_beam.plot(
                x,
                0,
                marker="o",
                markersize=10
            )

        elif support.support_type == SupportType.FIXED:

            ax_beam.plot(
                [x, x],
                [-0.3, 0.3],
                linewidth=3
            )

    # Внутренние шарниры
    for hinge in beam.internal_hinges:

        x = hinge.position

        ax_beam.plot(
            x,
            0,
            marker="o",
            markersize=8,
            markerfacecolor="white"
        )

    # Сечение для M, Q и D
    if (
        section_position is not None
        and quantity in ("M", "Q", "D")
    ):

        ax_beam.axvline(
            section_position,
            linestyle="--",
            linewidth=1
        )

        ax_beam.text(
            section_position,
            0.35,
            f"x = {section_position:.2f} м",
            ha="center"
        )

    # Опора для R
    if (
        section_position is not None
        and quantity == "R"
    ):

        ax_beam.text(
            section_position,
            0.35,
            f"R, x = {section_position:.2f} м",
            ha="center"
        )

    # ==================================================
    # СТРЕЛКА ЕДИНИЧНОЙ НАГРУЗКИ
    # ==================================================

    load_arrow = ax_beam.arrow(
        positions[0],
        0.8,
        0,
        -0.6,
        head_width=0.12,
        head_length=0.15,
        length_includes_head=True
    )

    load_text = ax_beam.text(
        positions[0],
        0.9,
        "P = 1",
        ha="center"
    )

    # Текущий результат
    result_text = ax_beam.text(
        0.02,
        0.95,
        "",
        transform=ax_beam.transAxes,
        ha="left"
    )

    ax_beam.set_xlim(
        -0.5,
        total_length + 0.5
    )

    ax_beam.set_ylim(
        -0.6,
        1.1
    )

    ax_beam.set_xlabel(
        "Координата, м"
    )

    ax_beam.set_yticks([])

    ax_beam.grid(
        True,
        axis="x"
    )

    # ==================================================
    # НИЖНИЙ ГРАФИК — ЛИНИЯ ВЛИЯНИЯ
    # ==================================================

    influence_point = None
    influence_point_left = None
    influence_point_right = None

    # ==================================================
    # M
    # ==================================================

    if quantity == "M":

        if values is None:
            raise ValueError(
                "Для M необходимо передать values."
            )

        ax_influence.plot(
            positions,
            values,
            linewidth=2,
            label="M"
        )

        influence_point, = ax_influence.plot(
            [positions[0]],
            [values[0]],
            marker="o",
            markersize=10
        )

        minimum_value = min(values)
        maximum_value = max(values)

        ylabel = "M"

        title = (
            "Линия влияния "
            "изгибающего момента M"
        )

    # ==================================================
    # Q
    # ==================================================

    elif quantity == "Q":

        if left_values is None:
            raise ValueError(
                "Для Q необходимо передать left_values."
            )

        if right_values is None:
            raise ValueError(
                "Для Q необходимо передать right_values."
            )

        ax_influence.plot(
            positions,
            left_values,
            linewidth=2,
            label="Q слева"
        )

        ax_influence.plot(
            positions,
            right_values,
            linewidth=2,
            label="Q справа"
        )

        influence_point_left, = ax_influence.plot(
            [positions[0]],
            [left_values[0]],
            marker="o",
            markersize=9
        )

        influence_point_right, = ax_influence.plot(
            [positions[0]],
            [right_values[0]],
            marker="o",
            markersize=9
        )

        minimum_value = min(
            min(left_values),
            min(right_values)
        )

        maximum_value = max(
            max(left_values),
            max(right_values)
        )

        ylabel = "Q"

        title = (
            "Линия влияния "
            "поперечной силы Q"
        )

        ax_influence.legend()

    # ==================================================
    # R
    # ==================================================

    elif quantity == "R":

        if values is None:
            raise ValueError(
                "Для R необходимо передать values."
            )

        ax_influence.plot(
            positions,
            values,
            linewidth=2,
            label="R"
        )

        influence_point, = ax_influence.plot(
            [positions[0]],
            [values[0]],
            marker="o",
            markersize=10
        )

        minimum_value = min(values)
        maximum_value = max(values)

        ylabel = "R"

        title = (
            "Линия влияния "
            "реакции опоры R"
        )

    # ==================================================
    # D — ПРОГИБ
    # ==================================================

    elif quantity == "D":

        if values is None:
            raise ValueError(
                "Для D необходимо передать values."
            )

        ax_influence.plot(
            positions,
            values,
            linewidth=2,
            label="D"
        )

        influence_point, = ax_influence.plot(
            [positions[0]],
            [values[0]],
            marker="o",
            markersize=10
        )

        minimum_value = min(values)
        maximum_value = max(values)

        ylabel = "D"

        title = (
            "Линия влияния "
            "прогиба D"
        )

    else:

        raise ValueError(
            'Сейчас поддерживаются только '
            '"M", "Q", "R" и "D".'
        )

    # ==================================================
    # НУЛЕВАЯ ЛИНИЯ
    # ==================================================

    ax_influence.axhline(
        0,
        linewidth=0.8
    )

    margin = max(
        0.1,
        (maximum_value - minimum_value) * 0.15
    )

    ax_influence.set_xlim(
        -0.5,
        total_length + 0.5
    )

    ax_influence.set_ylim(
        minimum_value - margin,
        maximum_value + margin
    )

    ax_influence.set_xlabel(
        "Положение единичной нагрузки, м"
    )

    ax_influence.set_ylabel(
        ylabel
    )

    ax_influence.set_title(
        title
    )

    ax_influence.grid(True)

    # ==================================================
    # АНИМАЦИЯ
    # ==================================================

    def update(frame):

        nonlocal load_arrow

        load_arrow.remove()

        x = positions[frame]

        load_arrow = ax_beam.arrow(
            x,
            0.8,
            0,
            -0.6,
            head_width=0.12,
            head_length=0.15,
            length_includes_head=True
        )

        load_text.set_position(
            (x, 0.9)
        )

        if quantity == "M":

            current_value = values[frame]

            result_text.set_text(
                f"x = {x:.2f} м    "
                f"M = {current_value:.3f}"
            )

            influence_point.set_data(
                [x],
                [current_value]
            )

            return (
                load_arrow,
                load_text,
                result_text,
                influence_point
            )

        if quantity == "Q":

            current_left = left_values[frame]
            current_right = right_values[frame]

            result_text.set_text(
                f"x = {x:.2f} м    "
                f"Q слева = {current_left:.3f}    "
                f"Q справа = {current_right:.3f}"
            )

            influence_point_left.set_data(
                [x],
                [current_left]
            )

            influence_point_right.set_data(
                [x],
                [current_right]
            )

            return (
                load_arrow,
                load_text,
                result_text,
                influence_point_left,
                influence_point_right
            )

        if quantity == "R":

            current_value = values[frame]

            result_text.set_text(
                f"x = {x:.2f} м    "
                f"R = {current_value:.3f}"
            )

            influence_point.set_data(
                [x],
                [current_value]
            )

            return (
                load_arrow,
                load_text,
                result_text,
                influence_point
            )

        if quantity == "D":

            current_value = values[frame]

            result_text.set_text(
                f"x = {x:.2f} м    "
                f"D = {current_value:.3f}"
            )

            influence_point.set_data(
                [x],
                [current_value]
            )

            return (
                load_arrow,
                load_text,
                result_text,
                influence_point
            )

    animation = FuncAnimation(
        fig,
        update,
        frames=len(positions),
        interval=300,
        repeat=True
    )

    plt.tight_layout()

    plt.show()

    return animation