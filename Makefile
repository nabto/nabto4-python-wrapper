.PHONY: build

all: build

check-twine:
	@echo Checking twine
	pip freeze | grep twine

build:
	@echo Building the library
	python setup.py sdist

check-dist:
	@echo Checking the distribution
	twine check dist/*

upload:
	@echo Uploading to PyPI
	twine upload -r testpypi dist/*

clean:
	@echo Clean up
	rm -rf build
	rm -rf dist
	rm -rf nabto_client.egg-info
