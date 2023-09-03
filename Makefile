test:
	@pytest ./src/tests -vv -rf --maxfail=1

reformat:
	@isort --line-length 100 .
	@black --line-length 100 .

clean:
	@find . -name "__pycache__" | xargs rm -rf
	@find . -name ".pytest_cache" | xargs rm -rf
	@find . -name ".mypy_cache" | xargs rm -rf
