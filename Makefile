.PHONY: build

all: swig build

check-swig:
	@echo Checking swig
	swig -version

check-twine:
	@echo Checking twine
	pip freeze | grep twine

swig:
	@echo swigging nabto_client/nabto_client.i to nabto_client/nabto_client_wrap.cpp
	swig -Wall -python -c++ -o nabto_client/nabto_client_wrap.cpp nabto_client/nabto_client.i

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
	rm nabto_client/nabto_api.py
	rm nabto_client/nabto_client_wrap.cpp
