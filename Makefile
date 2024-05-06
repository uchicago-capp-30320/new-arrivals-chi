# Here is some general information on Makefile's so that you can grow this out:
# https://www.gnu.org/software/make/manual/html_node/Introduction.html
default: create_requirements lint

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: create_requirements
create_requirements:
	poetry export --without-hashes --format=requirements.txt > requirements.txt
