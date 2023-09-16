
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
    poetry run ./tests/integration.py

# run the standard tests (default target)
test:
    rm -f data/*-test.json
    poetry run pytest --cov=petnet_app/ --cov-branch tests/

# run the standard tests + clippy and fmt
cover:
    poetry run coverage report -m
    poetry run coverage html --title="PetNetApp Test Coverage"

# invoke black, isort, ruff with --fix flag
format:
    black petnet_app/ tests/
    isort petnet_app/
    poetry run ruff check --fix ./petnet_app/

# run ruff (no fix)
ruff:
    poetry run ruff check ./petnet_app/

# ruff and pylint
lint:
    poetry run ruff check ./petnet_app/
    poetry run pylint ./petnet_app/

# dump the TODO hits
todos:
    rg TODO petnet_app/*.py tests/*.py

# run mypy
mypy:
    poetry run mypy petnet_app/

# runs refurb (slow)
refurb:
    poetry run refurb petnet_app/ tests/

# watch src and test ; run tests on change
watch:
    watchexec -c -w petnet_app/ -w tests/ -e .py -d 500 'just test lint'
    
# launch bpython and start with .repl-start.py script
repl:
    poetry run bpython -i .repl-start.py

# precommit tasks including test, cover, format, ruff, refurb and mypy
precommit:
    clear
    just test cover format lint refurb mypy

