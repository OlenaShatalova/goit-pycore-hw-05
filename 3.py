import sys
from pathlib import Path
from datetime import datetime

VALID_LEVELS = {"INFO", "DEBUG", "ERROR", "WARNING"}

def parse_log_line(line: str) -> dict:
    """
    Парсить один рядок лог-файлу.

    Очікуваний формат:
    YYYY-MM-DD HH:MM:SS LEVEL message

    Перевіряє:
        - формат дати
        - формат часу
        - коректність рівня логування

    Повертає словник з полями: date, time, level, message
    """

    parts = line.strip().split(maxsplit=3)

    if len(parts) < 4:
        raise ValueError(f"Неправильний формат рядка логу: {line}")

    date, time, level, message = parts
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Неправильний формат дати в файлі логування: {date}")
    try:
        datetime.strptime(time, "%H:%M:%S")
    except ValueError:
        raise ValueError(f"Неправильний формат часу в файлі логування: {time}")
    if level not in VALID_LEVELS:
        raise ValueError(f"Невідомий рівень логування в файлі логування: {level}")

    return {
        "date":date,
        "time": time,
        "level": level,
        "message": message
    }

def load_logs(file_path: str) -> list:
    """
     Зчитує лог-файл та перетворює кожен рядок у словник.
     Використовує функцію parse_log_line для обробки кожного рядка.
     Повертає список словників з логами.
     """
    load_logs = Path(file_path).read_text(encoding="utf-8")
    logs = [parse_log_line(line) for line in load_logs.splitlines()]
    return logs

def filter_logs_by_level(logs: list, level: str) -> list:
    """
    Фільтрує список логів за заданим рівнем логування.
    Повертає список логів, які відповідають заданому рівню.
    """
    return list(filter(lambda log: log["level"] == level, logs))

def count_logs_by_level(logs: list) -> dict:
    """
    Підраховує кількість логів для кожного рівня логування.
    Повертає словник: {LEVEL: count}
    """

    counts = {}
    for log in logs:
        level = log["level"]
        counts[level] = counts.get(level, 0) + 1
    return counts

def display_log_counts(counts: dict):
    """
    Виводить таблицю з кількістю логів для кожного рівня.
    """

    print("Рівень логування | Кількість")
    print("-----------------|----------")
    for level, count in counts.items():
        print(f"{level:<16} | {count}")


def main():
    """
    Головна функція програми.

    Виконує:
       - зчитування аргументів командного рядка
       - завантаження логів
       - підрахунок логів за рівнем
       - виведення статистики
       - фільтрацію логів (якщо передано рівень)
    """

    if len(sys.argv) < 2:
        print("Введіть за зразком: python 3.py logfile.log [error](не обовʼязково)")
        return

    file_path = sys.argv[1]

    try:
        logs = load_logs(file_path)
    except FileNotFoundError:
        print(f"Файл '{file_path}' не знайдено.")
        return
    except PermissionError:
        print(f"Немає доступу до файлу '{file_path}'.")
        return
    except UnicodeDecodeError:
        print("Помилка читання файлу: неправильне кодування.")
        return
    except Exception as e:
        print(f"Сталася помилка: {e}")
        return

    log_counts = count_logs_by_level(logs)
    display_log_counts(log_counts)

    if len(sys.argv) > 2:
        level = sys.argv[2].upper()

        if level not in VALID_LEVELS:
            print("\nНевірний рівень логування.")
            print("Доступні рівні:", ", ".join(sorted(VALID_LEVELS)))
            return

        filtered_logs = filter_logs_by_level(logs, level)

        print(f"\nДеталі логів для рівня '{level}':")

        for log in filtered_logs:
            print(f"{log['date']} {log['time']} - {log['message']}")

if __name__ == "__main__":
    main()

# python 3.py logfile.log
# python 3.py logfile.log error
