build:
	docker build . -t kevin91nl/entity-salience
push:
	docker push kevin91nl/entity-salience
checks:
	flake8
	touch __init__.py
	trap "rm __init__.py" EXIT
	pylint /code
	pydocstyle --convention=numpy --match-dir "^(?!migrations|node_modules|\.git|sandbox|Trash).*"
	pytest tests