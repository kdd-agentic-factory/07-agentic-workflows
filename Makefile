.PHONY: validate test lint install clean

install:
	pip install pyyaml jsonschema pytest

validate:
	python validators/validate_workflow_schema.py
	python validators/validate_approval_gates.py
	python validators/validate_required_artifacts.py
	python validators/validate_workflow_catalog.py
	python validators/validate_workflow_dependencies.py

test:
	python -m pytest tests/ -v

lint:
	python -m py_compile validators/*.py tests/*.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
