VENV := .venv

.venv:
	poetry install --no-root
	poetry check

setup: .venv

split:
	python src/split_datasets.py
