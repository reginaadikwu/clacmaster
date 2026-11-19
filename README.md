# CalcMaster

**CalcMaster** is an all-in-one calculator application built with Python. It is designed to provide basic and scientific calculations through multiple interfaces.

The project is being developed in phases, starting with a Python calculation engine and expanding into web and desktop applications.

## Project Features

### 1. Basic Calculator
- Addition
- Subtraction
- Multiplication
- Division
- Division-by-zero protection
- Invalid-operation handling

### 2. Scientific Calculator
- Powers and exponents
- Square roots
- Logarithms
- Sine
- Cosine
- Tangent
- Mathematical constants (Pi and Euler's number)

### 3. Web Application
- Built with Python and Flask
- Browser-based calculator interface
- Supports basic and scientific calculations

### 4. Desktop Application
- Built with Python and Tkinter
- Graphical calculator interface
- Basic and scientific calculation features
- Keyboard interaction support

## Project Structure

```text
clacmaster/
│
├── calculator.py
├── scientific_calculator.py
├── main.py
├── desktop_app.py
│
├── web/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── style.css
│       └── script.js
│
├── tests/
│   ├── test_calculator.py
│   └── test_scientific_calculator.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

- Python 3.8 or higher
- Flask 3.1.3
- Tkinter for the desktop application

The basic and scientific calculation engines use Python's standard library. Flask is required for the web application.

Tkinter may need to be installed separately through your operating system's package manager.

## Installation

Clone the repository:

```bash
git clone https://github.com/reginaadikwu/clacmaster.git
```

Enter the project directory:

```bash
cd clacmaster
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

### Run the Python Calculator

```bash
python3 main.py
```

### Run the Web Application

```bash
python3 web/app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

This runs the Flask development server locally. It is not intended for production deployment.

### Run the Desktop Application

```bash
python3 desktop_app.py
```

Make sure Tkinter is installed and available in your Python environment before launching the desktop application.

## Running Tests

Run the automated test suite:

```bash
python3 -m unittest discover -s tests -v
```

The tests cover the basic and scientific calculation engines.

## Development Roadmap

| Phase | Description | Status |
|---|---|---|
| Phase 1 | Basic Calculation Engine | Completed |
| Phase 2 | Scientific Calculator Engine | Completed |
| Phase 3 | Web Application | Completed |
| Phase 4 | Desktop Application | Code completed; GUI runtime testing pending |
| Phase 5 | Calculation History and Saved Calculations | Planned |
| Phase 6 | Final Testing, Security, Documentation and Deployment Preparation | Planned |

## Project Goal

The long-term goal is to develop CalcMaster into a reliable calculator platform that can grow across desktop, web and mobile environments while sharing a common calculation engine.

## Author

**Regina Adikwu**

GitHub: [reginaadikwu](https://github.com/reginaadikwu)

## License

A license has not yet been selected for this project.
