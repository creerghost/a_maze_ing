PYTHON = python3
PIP = pip
MAIN_SCRIPT = a_maze_ing.py
CONFIG_FILE = config.txt

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(MAIN_SCRIPT) $(CONFIG_FILE)

debug:
	$(PYTHON) -m pdb $(MAIN_SCRIPT) $(CONFIG_FILE)

clean:
	rm -rf __pycache__ .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
	flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	flake8 .
	mypy --strict .
