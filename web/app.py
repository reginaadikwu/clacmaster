
import sys
from pathlib import Path

from flask import Flask, render_template, request

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

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        operation = request.form.get("operation", "")

        try:
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

        except (ValueError, KeyError, TypeError):
            result = "Error: Please enter valid numbers"

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
