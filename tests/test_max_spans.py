from model.beam import Beam


beam = Beam()

print("\n=== ПРОВЕРКА МАКСИМАЛЬНОГО ЧИСЛА ПРОЛЁТОВ ===")

for i in range(5):
    beam.add_span(3.0)

print(
    f"Количество пролётов: "
    f"{len(beam.spans)}"
)

assert len(beam.spans) == 5

print("✓ 5 пролётов добавлены")


try:

    beam.add_span(3.0)

    raise AssertionError(
        "Шестой пролёт был добавлен."
    )

except ValueError as error:

    print(
        f"✓ Шестой пролёт отклонён: {error}"
    )


print("\nПРОВЕРКА ПРОЙДЕНА ✓")