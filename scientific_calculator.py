import math


def power(base, exponent):
    try:
        result = math.pow(base, exponent)
        return result
    except (ValueError, OverflowError):
        return "Error: Invalid power operation"


def square_root(number):
    if number < 0:
        return "Error: Cannot calculate square root of a negative number"

    return math.sqrt(number)


def logarithm(number, base=10):
    if number <= 0:
        return "Error: Logarithm requires a positive number"

    if base <= 0 or base == 1:
        return "Error: Logarithm base must be positive and not 1"

    return math.log(number, base)


def sine(angle):
    return math.sin(math.radians(angle))


def cosine(angle):
    return math.cos(math.radians(angle))


def tangent(angle):
    radians = math.radians(angle)

    if math.isclose(math.cos(radians), 0, abs_tol=1e-12):
        return "Error: Tangent is undefined at this angle"

    return math.tan(radians)


def get_constant(name):
    constants = {
        "pi": math.pi,
        "e": math.e
    }

    return constants.get(name.lower(), "Invalid constant")
