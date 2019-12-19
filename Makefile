.PHONY: build

all: build

build:
	@echo Building the library
	swig -Wall -python nabto_client.i
	python setup.py build_ext --inplace

clean:
	rm -f nabto_client_wrap.c
	rm -f nabto_api.py
	rm -rf nabto_client.egg-info