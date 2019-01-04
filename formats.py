import babel.numbers


def money(value):
    return babel.numbers.format_currency(number=value, currency="USD", locale='en_US')


def percentage(value):
    return '{:.1%}'.format(value)
