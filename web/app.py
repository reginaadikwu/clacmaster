import sys
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for

# Make the project root accessible to Python
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from calculator import calculate

from scientific_calculator import (
    power,
    square_root,
    logarithm,
    sine,
    cosine,
    tangent,
    get_constant,
)

from database import initialize_database

from history import (
    add_calculation,
    get_calculation_history,
    get_calculation_by_id,
    delete_calculation,
    clear_calculation_history,
)

from saved_calculations import (
    save_calculation,
    get_saved_calculations,
    delete_saved_calculation,
)

app = Flask(__name__)

# Create the database tables when the application starts
initialize_database()


def is_successful_result(result):
    """Check whether a calculation produced a valid result."""

    if result is None:
        return False

    if isinstance(result, str):
        if result.startswith("Error:") or result == "Invalid operation":
            return False

    return True


def build_expression(operation, a=None, b=None, base=None, name=None):
    """Build a readable expression for calculation history."""

    symbols = {
        "add": "+",
        "subtract": "-",
        "multiply": "×",
        "divide": "÷",
        "power": "^",
    }

    if operation in symbols:
        return f"{a} {symbols[operation]} {b}"

    if operation == "square_root":
        return f"√({a})"

    if operation == "logarithm":
        return f"log base {base} of {a}"

    if operation in ("sine", "cosine", "tangent"):
        return f"{operation}({a}°)"

    if operation == "constant":
        return f"Constant: {name}"

    return operation


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    expression = None
    calculation_id = None

    if request.method == "POST":
        operation = request.form.get("operation", "")

        try:
            a = None
            b = None
            base = None
            name = None

            if operation in ("add", "subtract", "multiply", "divide"):
                a = float(request.form["number"])
                b = float(request.form["second_number"])

                result = calculate(operation, a, b)

            elif operation == "power":
                a = float(request.form["number"])
                b = float(request.form["second_number"])

                result = power(a, b)

            elif operation == "square_root":
                a = float(request.form["number"])
                result = square_root(a)

            elif operation == "logarithm":
                a = float(request.form["number"])
                base = float(request.form.get("base") or 10)

                result = logarithm(a, base)

            elif operation in ("sine", "cosine", "tangent"):
                a = float(request.form["number"])

                functions = {
                    "sine": sine,
                    "cosine": cosine,
                    "tangent": tangent,
                }

                result = functions[operation](a)

            elif operation == "constant":
                name = request.form["constant_name"]
                result = get_constant(name)

            else:
                result = "Invalid operation"

            expression = build_expression(
                operation,
                a=a,
                b=b,
                base=base,
                name=name,
            )

            # Record only successful calculations
            if is_successful_result(result):
                calculation_id = add_calculation(operation, expression, result)

        except (ValueError, KeyError, TypeError):
            result = "Error: Please enter valid numbers"

    history = get_calculation_history()
    saved_calculations = get_saved_calculations()

    return render_template(
        "index.html",
        result=result,
        expression=expression,
        calculation_id=calculation_id,
        history=history,
        saved_calculations=saved_calculations,
    )


@app.route("/history/<int:calculation_id>/delete", methods=["POST"])
def remove_history(calculation_id):
    delete_calculation(calculation_id)
    return redirect(url_for("home"))


@app.route("/history/clear", methods=["POST"])
def clear_history():
    clear_calculation_history()
    return redirect(url_for("home"))


@app.route("/saved", methods=["POST"])
def save_current_calculation():
    title = request.form.get("title", "").strip()
    calculation_id = request.form.get("calculation_id", "")

    try:
        if not title:
            raise ValueError("Title cannot be empty")

        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters")

        if not calculation_id.isdigit():
            raise ValueError("Invalid calculation ID")

        calculation = get_calculation_by_id(int(calculation_id))

        if calculation is None:
            raise ValueError("Calculation not found")

        save_calculation(
            title,
            calculation["expression"],
            calculation["result"],
        )

    except ValueError:
        pass

    return redirect(url_for("home"))

@app.route("/saved/<int:calculation_id>/delete", methods=["POST"])
def remove_saved_calculation(calculation_id):
    delete_saved_calculation(calculation_id)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
