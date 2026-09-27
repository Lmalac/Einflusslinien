import numpy as np


def prepare_influence_data(result: dict) -> dict:
    """
    Подготавливает результат линии влияния
    для передачи в интерфейс.

    Поддерживаемые величины:
        R — реакция
        M — изгибающий момент
        Q — поперечная сила
        D — прогиб
    """

    if not isinstance(result, dict):
        raise ValueError(
            "Результат расчёта должен быть словарём."
        )

    if "quantity" not in result:
        raise ValueError(
            "В результате отсутствует величина quantity."
        )

    if "positions" not in result:
        raise ValueError(
            "В результате отсутствуют координаты positions."
        )

    quantity = result["quantity"].upper()

    positions = np.asarray(
        result["positions"],
        dtype=float
    )

    if quantity in ("R", "M", "D"):

        if "values" not in result:
            raise ValueError(
                "В результате отсутствуют значения values."
            )

        values = np.asarray(
            result["values"],
            dtype=float
        )

        if len(positions) != len(values):
            raise ValueError(
                "Количество координат не совпадает "
                "с количеством значений."
            )

        return {
            "quantity": quantity,
            "positions": positions.tolist(),
            "values": values.tolist()
        }

    if quantity == "Q":

        if "left_values" not in result:
            raise ValueError(
                "В результате отсутствуют left_values."
            )

        if "right_values" not in result:
            raise ValueError(
                "В результате отсутствуют right_values."
            )

        left_values = np.asarray(
            result["left_values"],
            dtype=float
        )

        right_values = np.asarray(
            result["right_values"],
            dtype=float
        )

        if len(positions) != len(left_values):
            raise ValueError(
                "Количество координат не совпадает "
                "с количеством left_values."
            )

        if len(positions) != len(right_values):
            raise ValueError(
                "Количество координат не совпадает "
                "с количеством right_values."
            )

        return {
            "quantity": quantity,
            "positions": positions.tolist(),
            "left_values": left_values.tolist(),
            "right_values": right_values.tolist()
        }

    raise ValueError(
        'Неизвестная величина. Используйте "R", "M", "Q" или "D".'
    )