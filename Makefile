FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
MYPY = uv run python -m mypy
FLAKE8 = uv run python -m flake8
MAIN = main.py
SRC = src/

install:
	@echo "Installing..."
	uv sync
	@echo "Installation done!"

run: install
	@echo "Running..."
	uv run python main.py $(ARGS)

debug: install
	@echo "Running in debug mode..."
	uv run python -m pdb main.py $(ARGS)

lint:
	@echo "Linting..."
	$(FLAKE8) $(MAIN) $(SRC)
	$(MYPY) $(FLAGS) $(MAIN) $(SRC)
	@echo "Linting Done!"

lint-strict:
	@echo "Linting stric mode..."
	$(FLAKE8) $(MAIN) $(SRC)
	$(MYPY) --strict $(MAIN) $(SRC)
	@echo "Linting Done!"

clean:
	@echo "Cleaning..."
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type d -name .mypy_cache -exec rm -rf {} +
	@echo "Cleaning done!"

.PHONY: install run lint lint-strict clean
