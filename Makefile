build:
	docker build . -t kevin91nl/entity-salience
push:
	docker push kevin91nl/entity-salience
run_checks:
	flake8
	find . -iname "*.py" ! -wholename "*node_modules*" ! -wholename "*migrations*" ! -wholename "*.git*" ! -wholename "*test_data*" ! -wholename "*tests*" ! -wholename "*manage.py*" ! -wholename "*sandbox*" | xargs pylint
	pydocstyle --convention=numpy --match-dir "^(?!migrations|node_modules|\.git|test_data|tests|sandbox|Trash).*"