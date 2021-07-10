VERSION=0.0.1

clean:
	rm -r *egg-info || true
	rm -r build || true
	rm -r dist || true

build:
	python3 setup.py sdist bdist_wheel

push:
	twine upload dist/*

test:
	pytest tests

format:
	black scraper