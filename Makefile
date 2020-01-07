.PHONY: build

all: swig build

swig:
	@echo swigging nabto_client/nabto_client.i to nabto_client/nabto_client_wrap.cpp
	swig -Wall -python -c++ -o nabto_client/nabto_client_wrap.cpp nabto_client/nabto_client.i
build:
	@echo Building the library using docker
	docker build -t nabto-client . && docker run -v `pwd`/dist:/nabto-client/dist nabto-client python setup.py sdist bdist_wheel

clean:
	rm -rf build
	rm -rf dist
	rm -rf nabto_client.egg-info
	rm nabto_client/nabto_api.py
	rm nabto_client/nabto_client_wrap.cpp