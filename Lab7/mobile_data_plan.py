
import math


def parse_plan(text):
    if not isinstance(text, str):
        raise ValueError("Input must be text")

    parts = text.split(':')
    if len(parts) != 2:
        raise ValueError("Enter plan and data separated by ':'")

    plan = parts[0].strip()
    if not plan:
        raise ValueError("Plan name cannot be empty")

    try:
        gb = float(parts[1])
    except ValueError:
        raise ValueError("Data amount must be a valid number")

    if not math.isfinite(gb) or gb <= 0:
        raise ValueError("Data amount must be positive and finite")

    return plan.title(), gb


def usage_average(usage_csv):
    if not isinstance(usage_csv, str) or not usage_csv.strip():
        raise ValueError("Usage data cannot be empty")

    try:
        values = [int(r.strip()) for r in usage_csv.split(',')]
    except ValueError:
        raise ValueError("Usage values must be integers")

    if not values:
        raise ValueError("At least one usage value is required")

    if any(value < 0 for value in values):
        raise ValueError("Usage values cannot be negative")

    return sum(values) // len(values)


def payable_bill(text):
    if not isinstance(text, str):
        raise ValueError("Input must be text")

    parts = text.split('|')
    if len(parts) != 2:
        raise ValueError("Enter bill and discount separated by '|'")

    try:
        bill = float(parts[0])
        discount = float(parts[1])
    except ValueError:
        raise ValueError("Bill and discount must be valid numbers")

    if not math.isfinite(bill) or not math.isfinite(discount):
        raise ValueError("Bill and discount must be finite")

    if bill < 0 or discount < 0:
        raise ValueError("Bill and discount cannot be negative")

    total = bill * 1.18 - discount
    return max(total, 0)


def main():
    print("==== Running parse_plan ====")
    user_input = input("Enter plan:data in GB (e.g. standard:5): ")
    result = parse_plan(user_input)
    print("Plan and Data:", result)

    print("\n==== Running usage_average ====")
    user_input = input("Enter daily usage in MB as CSV (e.g. 300,450,800): ")
    result = usage_average(user_input)
    print("Average Usage:", result)

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 399|50): ")
    result = payable_bill(user_input)
    print("Payable Bill:", result)


if __name__ == "__main__":
    main()
