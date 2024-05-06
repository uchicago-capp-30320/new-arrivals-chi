default: create_requirements lint

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: create_requirements
create_requirements:
	poetry export --without-hashes --format=requirements.txt > requirements.txt
