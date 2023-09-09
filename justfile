
project := "petnet_app"

export PYTHONPATH := "petnet_app/"

alias int := integration
alias cov := cover
alias form := format
alias pre := precommit
alias todo := todos

# run the application
run:
    poetry run uvicorn petnet_app.main:app --port 9001 --reload

# run the integration tests
integration:
    poetry run ./tests/integration.py --verbose

# run the standard tests (default target)
test:
    poetry run pytest --cov=petnet_app/ --cov-branch tests/

# run the standard tests + clippy and fmt
cover:
    poetry run coverage report -m
    poetry run coverage html --title="PetNetApp Test Coverage"

format:
    black petnet_app/ tests/
    isort petnet_app/
    poetry run ruff check --fix ./petnet_app/

ruff:
    poetry run ruff check ./petnet_app/

lint:
    poetry run ruff check ./petnet_app/
    poetry run pylint ./petnet_app/

todos:
    rg TODO petnet_app/*.py tests/*.py

mypy:
    poetry run mypy petnet_app/

refurb:
    poetry run refurb petnet_app/ tests/


precommit:
    clear
    just test cover format ruff refurb mypy

