run:
	py main.py

docs:
	@python -m pydoc -w main

.PHONY: run docs
