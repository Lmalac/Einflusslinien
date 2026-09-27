from model.beam import Beam, SupportType


beam = Beam()

beam.add_span(6.0, 1.0)

print("\n=== ПРОВЕРКА АВТОМАТИЧЕСКОГО УЗЛА ОПОРЫ ===")

print("\nДо добавления опоры:")
print(f"Количество пролётов: {len(beam.spans)}")

beam.add_support(
    3.0,
    SupportType.ROLLER
)

print("\nПосле добавления опоры x = 3 м:")
print(f"Количество пролётов: {len(beam.spans)}")

print("\nПролёты:")

current_position = 0.0

for index, span in enumerate(beam.spans, start=1):

    start = current_position
    end = current_position + span.length

    print(
        f"Пролёт {index}: "
        f"{start:.2f} — {end:.2f} м"
    )

    current_position = end


assert len(beam.spans) == 2

assert abs(beam.spans[0].length - 3.0) < 1e-9
assert abs(beam.spans[1].length - 3.0) < 1e-9

print("\n✓ Опора автоматически создала узел")
print("✓ Пролёт разбит на два элемента")
print("\nПРОВЕРКА ПРОЙДЕНА ✓")