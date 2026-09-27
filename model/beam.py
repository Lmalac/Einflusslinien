from dataclasses import dataclass
from enum import Enum


class SupportType(Enum):
    PINNED = "шарнирно-неподвижная"
    ROLLER = "шарнирно-подвижная"
    FIXED = "заделка"
    FREE = "свободный конец"


@dataclass
class Span:
    length: float
    relative_ei: float = 1.0

    def __post_init__(self):
        if self.length <= 0:
            raise ValueError("Длина пролёта должна быть больше нуля.")

        if self.relative_ei <= 0:
            raise ValueError("Относительная жёсткость EI должна быть больше нуля.")


@dataclass
class Support:
    position: float
    support_type: SupportType


@dataclass
class InternalHinge:
    position: float


class Beam:
    MAX_SPANS = 5

    def __init__(self):
        self.spans: list[Span] = []
        self.supports: list[Support] = []
        self.internal_hinges: list[InternalHinge] = []

    def add_span(self, length: float, relative_ei: float = 1.0):
        if len(self.spans) >= self.MAX_SPANS:
            raise ValueError("Максимальное количество пролётов — 5.")

        self.spans.append(Span(length, relative_ei))

    @property
    def total_length(self) -> float:
        return sum(span.length for span in self.spans)
######################################################################
    def add_support(
            self,
            position: float,
            support_type: SupportType
    ):
        if position < 0 or position > self.total_length:
            raise ValueError(
                "Положение опоры должно находиться в пределах балки."
            )

        # Опора должна находиться в узле FEM-модели.
        if position > 0 and position < self.total_length:
            self.insert_node(position)

        self.supports.append(
            Support(position, support_type)
        )

    def add_internal_hinge(self, position: float):
        if position <= 0 or position >= self.total_length:
            raise ValueError(
                "Внутренний шарнир должен находиться внутри балки."
            )

        # Шарнир должен находиться в узле FEM-модели.
        self.insert_node(position)

        self.internal_hinges.append(
            InternalHinge(position)
        )
####################################################
    def is_internal_hinge(self, position: float) -> bool:
        """
        Проверяет, находится ли внутренний шарнир
        в заданной координате.
        """

        tolerance = 1e-9

        return any(
            abs(hinge.position - position) < tolerance
            for hinge in self.internal_hinges
        )
#################################################


    def print_scheme(self):
        print("\n=== РАСЧЁТНАЯ СХЕМА ===")

        print(f"Количество пролётов: {len(self.spans)}")
        print(f"Общая длина: {self.total_length:.2f} м")

        print("\nПролёты:")

        current_position = 0.0

        for i, span in enumerate(self.spans, start=1):
            start = current_position
            end = current_position + span.length

            print(
                f"  Пролёт {i}: "
                f"{start:.2f} — {end:.2f} м | "
                f"L = {span.length:.2f} м | "
                f"EI = {span.relative_ei:.3f}"
            )

            current_position = end

        print("\nОпоры:")

        for support in self.supports:
            print(
                f"  x = {support.position:.2f} м — "
                f"{support.support_type.value}"
            )

        print("\nВнутренние шарниры:")

        if self.internal_hinges:
            for hinge in self.internal_hinges:
                print(
                    f"  x = {hinge.position:.2f} м"
                )
        else:
            print("  нет")

    def insert_node(self, position: float):
        """
        Добавляет узел в заданной координате балки.

        Если точка находится внутри пролёта,
        пролёт разбивается на два пролёта.
        """

        if position <= 0 or position >= self.total_length:
            raise ValueError(
                "Новый узел должен находиться внутри балки."
            )

        current_position = 0.0

        for index, span in enumerate(self.spans):

            start = current_position
            end = current_position + span.length

            # Точка уже является границей пролёта
            if abs(position - start) < 1e-9:
                return

            if abs(position - end) < 1e-9:
                return

            # Точка находится внутри пролёта
            if start < position < end:
                left_length = position - start
                right_length = end - position

                left_span = Span(
                    length=left_length,
                    relative_ei=span.relative_ei
                )

                right_span = Span(
                    length=right_length,
                    relative_ei=span.relative_ei
                )

                self.spans[index:index + 1] = [
                    left_span,
                    right_span
                ]

                return

            current_position = end

        raise ValueError(
            f"Не удалось добавить узел в x = {position}."
        )

    def copy(self):
        """
        Создаёт независимую копию расчётной схемы балки.
        """

        new_beam = Beam()

        # `self.spans` may include FEM subspans created when supports
        # or internal hinges split the original physical spans. Copy these
        # directly: the five-span limit applies to user-defined spans, not
        # to the extra segments in the discretized calculation model.
        new_beam.spans = [
            Span(span.length, span.relative_ei)
            for span in self.spans
        ]

        for support in self.supports:
            new_beam.add_support(
                support.position,
                support.support_type
            )

        for hinge in self.internal_hinges:
            new_beam.add_internal_hinge(
                hinge.position
            )

        return new_beam
