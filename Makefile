install:
	uv sync

run:
	uv run python main.py

lint:
	uv run python -m flake8 main.py src/
	uv run python -m mypy main.py src/
