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

docs:
	touch nabto_client/nabto.py
	pdoc --html --force nabto_client
	rm nabto_client/nabto.py

clean:
	@echo Clean up
	rm -rf build
	rm -rf dist
	rm -rf nabto_client.egg-info
	rm -rf html
