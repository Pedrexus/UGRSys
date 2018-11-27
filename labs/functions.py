from decimal import Decimal


def p2f(string):
    """convert percentage string to float

    string :param e.g.: '59%'
    float :return e.g.: 0.59

    """
    return float(string.strip('%')) / 100


def p2d(string):
    """convert percentage string to decimal.Decimal"""

    return Decimal(p2f(string))
