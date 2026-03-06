import re
from typing import Callable

def generator_numbers(text: str):
    """Extract float numbers from text and yield them one by one."""
    pattern = r"\d+\.\d+"
    matches = re.findall(pattern, text)

    # Yield each number as float
    for num in matches:
        yield float(num)

def sum_profit(text: str, func: Callable) -> float:
    """Calculate the total sum of numbers produced by the generator."""
    numbers = func(text)
    return sum(numbers)


text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")
