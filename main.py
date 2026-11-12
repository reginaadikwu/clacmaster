from calculator import calculate

from scientific_calculator import (
    power,
    square_root,
    logarithm,
    sine,
    cosine,
    tangent,
    get_constant
)


def main():
    print("================================")
    print("       WELCOME TO CALCMASTER")
    print("================================")

    print("\n--- BASIC CALCULATIONS ---")

    print("Addition:", calculate("add", 10, 5))
    print("Subtraction:", calculate("subtract", 10, 5))
    print("Multiplication:", calculate("multiply", 10, 5))
    print("Division:", calculate("divide", 10, 5))

    print("\n--- SCIENTIFIC CALCULATIONS ---")

    print("Power:", power(2, 3))
    print("Square root:", square_root(25))
    print("Logarithm:", logarithm(100))
    print("Sine:", sine(30))
    print("Cosine:", cosine(60))
    print("Tangent:", tangent(45))

    print("\n--- SCIENTIFIC CONSTANTS ---")

    print("Pi:", get_constant("pi"))
    print("Euler's number:", get_constant("e"))


if __name__ == "__main__":
    main()
