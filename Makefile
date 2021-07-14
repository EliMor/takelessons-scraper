VERSION=$(shell head -n 1 takelessons_scraper/__version__ | sed 's/v//')

clean:
	rm -r *egg-info || true
	rm -r build || true
	rm -r dist || true

install:
	python3 setup.py install

build:
	python3 setup.py sdist bdist_wheel

push:
	twine upload dist/*

test:
	pytest tests

format:
	black takelessons_scraper