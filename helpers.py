def inflate_value(initial: float, inflation_rate, count):
    result = []
    current_value = initial
    multiplier = (1 + inflation_rate)
    for i in range(count):
        result.append(current_value)
        current_value = current_value * multiplier
    return result
