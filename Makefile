default: lint create_requirements

.PHONY: create_requirements
create_requirements:
	poetry export --without-hashes --format=requirements.txt > requirements.txt

.PHONY: update_db
update_db:
	web alembic --config=./new_arrivals_chi/app/migrations/alembic.ini upgrade head

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: test
test: # Runs all tests
	pytest tests -vs

.PHONY: stamp_db
stamp_db: # Runs the stamp command to set the base state of the db
	alembic --config=./new_arrivals_chi/app/migrations/alembic.ini stamp head

.PHONY: create_revision
create_revision: # Runs the command that creates the Alembic revision
	alembic --config=./new_arrivals_chi/app/migrations/alembic.ini revision --autogenerate
