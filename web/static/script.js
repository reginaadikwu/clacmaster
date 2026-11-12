
const operation = document.getElementById("operation");

const numberField = document.getElementById("number");
const secondNumberField = document.getElementById("second_number");
const baseField = document.getElementById("base");
const constantField = document.getElementById("constant_name");

function updateFields() {
    const selected = operation.value;

    secondNumberField.style.display =
        ["add", "subtract", "multiply", "divide", "power"].includes(selected)
            ? "block" : "none";

    baseField.style.display =
        selected === "logarithm" ? "block" : "none";

    constantField.style.display =
        selected === "constant" ? "block" : "none";

    numberField.style.display =
        selected === "constant" ? "none" : "block";
}

operation.addEventListener("change", updateFields);

updateFields();
