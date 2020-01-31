.PHONY: build

all: build

check-twine:
	@echo Checking twine
	@if pip freeze | grep twine; then\
		echo "twine is installed";\
	else\
		echo "Use 'pip install twine' to install twine";\
	fi

build:
	@echo Building the library
	python setup.py sdist

check-dist:
	@echo Checking the distribution
	twine check dist/*

upload: check-twine build check-dist
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
