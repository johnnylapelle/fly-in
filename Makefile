FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
MYPY = uv run python -m mypy
FLAKE8 = uv run python -m flake8
MAIN = main.py
SRC = src/

install:
	uv sync

run:
	uv run python main.py $(MAP)

lint:
	$(FLAKE8) $(MAIN) $(SRC)
	$(MYPY) $(FLAGS) $(MAIN) $(SRC)

lint-strict:
	$(FLAKE8) $(MAIN) $(SRC)
	$(MYPY) --strict $(MAIN) $(SRC)

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +

.PHONY: install run lint lint-strict clean
