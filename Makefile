code-check:		## Check and format code using pre-commit
	pre-commit install
	pre-commit autoupdate
	pre-commit run --all-files

psql:
	docker-compose exec db psql --username=hello_fastapi --dbname=hello_fastapi_dev

enter:
	docker-compose exec web sh