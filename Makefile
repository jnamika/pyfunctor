.PHONY: all
all: 
	python setup.py sdist


.PHONY: test
test: 
	python setup.py test

.PHONY: clean
clean:
	rm -rf dist pyfunctor.egg-info
