
all: install

deps:
	pip install -r requirements.txt --user

install:
	pip install . --user --upgrade

uninstall:
	pip uninstall scene_generator

test:
	nosetests --rednose tests

.PHONY: init install uninstall test