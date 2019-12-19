.PHONY: build

all: build

build:
	@echo Building the library
	python setup.py bdist_wheel

clean:
	rm -rf build
	rm -rf dist
	rm -rf nabto_client.egg-info