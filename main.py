from calculator import calculate


def main():
    print("================================")
    print("       WELCOME TO CALCMASTER")
    print("================================")

    print("Addition:", calculate("add", 10, 5))
    print("Subtraction:", calculate("subtract", 10, 5))
    print("Multiplication:", calculate("multiply", 10, 5))
    print("Division:", calculate("divide", 10, 5))

    print("Division by zero:", calculate("divide", 10, 0))
    print("Invalid operation:", calculate("power", 10, 5))


if __name__ == "__main__":
    main()