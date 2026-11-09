import tkinter as tk
from calculator import calculate


class CalcMasterDesktop:

    def __init__(self, root):
        self.root = root
        self.root.title("CalcMaster")
        self.root.geometry("360x540")
        self.root.resizable(False, False)
        self.root.configure(bg="#172033")

        self.display = tk.StringVar(value="0")

        self.first_operand = None
        self.pending_operator = None
        self.start_new_number = True

        self.create_interface()

        self.root.bind("<Key>", self.handle_key)

    def create_interface(self):

        title = tk.Label(
            self.root,
            text="CalcMaster",
            font=("Arial", 22, "bold"),
            bg="#172033",
            fg="white"
        )
        title.pack(pady=(20, 10))

        display = tk.Entry(
            self.root,
            textvariable=self.display,
            font=("Arial", 30),
            justify="right",
            state="readonly",
            readonlybackground="#25324a",
            fg="white",
            bd=0
        )
        display.pack(
            fill="x",
            padx=15,
            ipady=20,
            pady=15
        )

        button_frame = tk.Frame(
            self.root,
            bg="#172033"
        )
        button_frame.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=10
        )

        buttons = [
            ["C", "⌫", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["±", "0", ".", "="],
            ["x²", "√x", "", ""]
        ]

        for row_index, row in enumerate(buttons):

            for column_index, value in enumerate(row):

                if value == "":
                    continue

                button = tk.Button(
                    button_frame,
                    text=value,
                    font=("Arial", 17, "bold"),
                    bg=self.button_color(value),
                    fg="white",
                    activebackground="#64748b",
                    activeforeground="white",
                    bd=0,
                    cursor="hand2",
                    command=lambda v=value: self.press(v)
                )

                button.grid(
                    row=row_index,
                    column=column_index,
                    padx=4,
                    pady=4,
                    sticky="nsew"
                )

        for column in range(4):
            button_frame.columnconfigure(
                column,
                weight=1
            )

        for row in range(6):
            button_frame.rowconfigure(
                row,
                weight=1
            )

        footer = tk.Label(
            self.root,
            text="Simple calculations. Smarter results.",
            font=("Arial", 9),
            bg="#172033",
            fg="#94a3b8"
        )
        footer.pack(pady=10)

    def button_color(self, value):

        if value in ["+", "−", "×", "÷", "="]:
            return "#2563eb"

        if value in ["C", "⌫"]:
            return "#dc3545"

        if value in ["%", "±", "x²", "√x"]:
            return "#475569"

        return "#334155"

    def format_result(self, value):

        if isinstance(value, float):
            return f"{value:.10g}"

        return str(value)

    def press(self, value):

        if value.isdigit():
            self.press_number(value)

        elif value == ".":
            self.press_decimal()

        elif value in ["+", "−", "×", "÷"]:
            self.press_operator(value)

        elif value == "=":
            self.press_equals()

        elif value == "C":
            self.clear()

        elif value == "⌫":
            self.backspace()

        elif value == "%":
            self.percentage()

        elif value == "x²":
            self.square()

        elif value == "√x":
            self.square_root()

        elif value == "±":
            self.toggle_sign()

    def press_number(self, number):

        current = self.display.get()

        if self.start_new_number or current == "Error":
            self.display.set(number)
            self.start_new_number = False

        else:
            if current == "0":
                self.display.set(number)
            else:
                self.display.set(current + number)

    def press_decimal(self):

        current = self.display.get()

        if self.start_new_number or current == "Error":
            self.display.set("0.")
            self.start_new_number = False

        elif "." not in current:
            self.display.set(current + ".")

    def press_operator(self, operator):

        try:
            current = float(self.display.get())

        except ValueError:
            return

        if self.pending_operator is not None:
            if not self.compute_pending():
                return

            current = float(self.display.get())

        self.first_operand = current
        self.pending_operator = operator
        self.start_new_number = True

    def compute_pending(self):

        if self.pending_operator is None:
            return True

        try:
            second_operand = float(self.display.get())

        except ValueError:
            return False

        operations = {
            "+": "add",
            "−": "subtract",
            "×": "multiply",
            "÷": "divide"
        }

        result = calculate(
            operations[self.pending_operator],
            self.first_operand,
            second_operand
        )

        if isinstance(result, str):
            self.display.set(result)
            self.pending_operator = None
            self.first_operand = None
            self.start_new_number = True
            return False

        self.display.set(self.format_result(result))
        self.first_operand = result

        return True

    def press_equals(self):

        if self.pending_operator is None:
            return

        self.compute_pending()

        self.pending_operator = None
        self.first_operand = None
        self.start_new_number = True

    def percentage(self):

        try:
            number = float(self.display.get())
            result = number / 100

            self.display.set(self.format_result(result))
            self.start_new_number = True

        except ValueError:
            self.clear()

    def square(self):

        try:
            number = float(self.display.get())
            result = number ** 2

            self.display.set(self.format_result(result))
            self.start_new_number = True

        except (ValueError, OverflowError):
            self.display.set("Error")
            self.start_new_number = True

    def square_root(self):

        try:
            number = float(self.display.get())

            if number < 0:
                self.display.set("Error")
                self.start_new_number = True
                return

            result = number ** 0.5

            self.display.set(self.format_result(result))
            self.start_new_number = True

        except (ValueError, OverflowError):
            self.display.set("Error")
            self.start_new_number = True

    def toggle_sign(self):

        try:
            number = float(self.display.get())

            self.display.set(self.format_result(-number))
            self.start_new_number = True

        except ValueError:
            return

    def backspace(self):

        current = self.display.get()

        if self.start_new_number or current == "Error":
            return

        if len(current) > 1:
            new_value = current[:-1]

            if new_value == "-":
                new_value = "0"

            self.display.set(new_value)

        else:
            self.display.set("0")

    def clear(self):

        self.display.set("0")
        self.first_operand = None
        self.pending_operator = None
        self.start_new_number = True

    def handle_key(self, event):

        key = event.char

        key_mapping = {
            "*": "×",
            "/": "÷",
            "-": "−"
        }

        if key.isdigit() or key == ".":
            self.press(key)

        elif key in ["+", "*", "/", "-"]:
            self.press(key_mapping.get(key, key))

        elif event.keysym in ["Return", "KP_Enter"]:
            self.press_equals()

        elif event.keysym == "BackSpace":
            self.backspace()

        elif event.keysym == "Escape":
            self.clear()

        return "break"


def main():

    root = tk.Tk()

    CalcMasterDesktop(root)

    root.mainloop()


if __name__ == "__main__":
    main()

