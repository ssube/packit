.PHONY: ci check-venv pip pip-dev lint-check lint-fix test typecheck package package-dist package-upload style

venv: ## create virtual env
	python3 -v venv venv

ci: pip pip-dev lint-check
	$(MAKE) test

check-venv:
	if [ -z $${VIRTUAL_ENV+x} ]; then echo "Are you sure you want to install dependencies outside of a virtual environment?"; sleep 30; fi

pip: check-venv
	pip install -r requirements/cpu.txt
	pip install -r requirements/base.txt

pip-dev: check-venv
	pip install -r requirements/dev.txt

test:
	python -m coverage erase
	python -m coverage run -m unittest discover -v -s tests/
	python -m coverage html -i
	python -m coverage xml -i
	python -m coverage report -i

coverage-report:
	python -m coverage html -i
	python -m coverage xml -i
	python -m coverage report -i

package: package-dist package-upload

package-dist:
	python3 ./setup.py sdist

package-upload:
	twine upload dist/*

lint-check:
	black --check packit/
	black --check examples/
	black --check tests/
	flake8 packit
	flake8 examples
	flake8 tests
	isort --check-only --skip __init__.py --filter-files packit
	isort --check-only --skip __init__.py --filter-files examples
	isort --check-only --skip __init__.py --filter-files tests

lint-fix:
	black packit/
	black examples/
	black tests/
	flake8 packit
	flake8 examples
	flake8 tests
	isort --skip __init__.py --filter-files packit
	isort --skip __init__.py --filter-files examples
	isort --skip __init__.py --filter-files tests

style: lint-fix

typecheck:
	mypy packit
