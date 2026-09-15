.PHONY: install run clean build check-python compile test unit-test integration-test docker-build docker-run

PYTHON ?= python
PYTHON_MIN_VERSION ?= 3.10

check-python:
	$(PYTHON) -c "import sys; minimum=tuple(map(int, '$(PYTHON_MIN_VERSION)'.split('.'))); version=sys.version_info[:2]; assert version >= minimum, f'Python {minimum[0]}.{minimum[1]} or newer is required, found {version[0]}.{version[1]}'"


install: check-python
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) -m src.server

clean:
	$(PYTHON) -c "from pathlib import Path; [file.unlink() for file in Path('.').rglob('*.pyc')]; [file.unlink() for file in Path('.').rglob('*.pyo')]; [directory.rmdir() for directory in sorted(Path('.').rglob('__pycache__'), reverse=True) if directory.is_dir()]"

compile:
	$(PYTHON) -m compileall -q src tests

unit-test:
	$(PYTHON) -m unittest discover -s tests/unit -v

integration-test:
	$(PYTHON) -m unittest discover -s tests/integration -v

test: unit-test integration-test

build: check-python compile test

docker-build:
	docker build -t tbdd-server .

docker-run:
	docker run --rm -p 8000:8000 tbdd-server
