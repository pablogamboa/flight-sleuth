format:
	@ruff --select I001 --fix .
	@ruff format --target-version py311 .
lint:
	@ruff .
fix:
	@ruff . --fix
typing:
	@mypy
unittest:
	@pytest -vs --disable-warnings --maxfail 1
