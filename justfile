
project := "petnet_app"

export PYTHONPATH := "petnet_app/"
export PYTHON := "/Library/Frameworks/Python.framework/Versions/3.11/bin/bpython"

alias int := integration
alias cov := cover
alias form := format
alias pre := precommit
alias todo := todos
alias sred := startTestRedis

# run the application
run:
    poetry run uvicorn petnet_app.main:app --port 9001 --reload

# run the integration tests
integration:
    poetry run ./tests/integration.py

# start the redis test server
startTestRedis:
    redis-server ./tests/redis-test.conf
    redis-cli -a testpw ping

stopTestRedis:
    redis-cli -a testpw shutdown

# run the standard tests (default target)
test $PETNET_DBHOST="localhost" $PETNET_DBAUTH="testpw" $PETNET_DBPORT="6379":
    /bin/rm -fr data
    /bin/rm -fr logs

    poetry run pytest --cov=petnet_app/ --cov-branch tests/

# run the standard tests + clippy and fmt
cover:
    poetry run coverage report -m
    poetry run coverage html --title="PetNetApp Test Coverage"

# invoke black, isort, ruff with --fix flag
format:
    poetry run black petnet_app/ tests/
    poetry run isort petnet_app/
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
precommit $PETNET_DBHOST="localhost" $PETNET_DBAUTH="testpw" $PETNET_DBPORT="6379":
    clear
    /bin/rm -fr data
    /bin/rm -fr logs

    poetry run pytest --cov=petnet_app/ --cov-branch tests/

    just cover format lint refurb mypy

