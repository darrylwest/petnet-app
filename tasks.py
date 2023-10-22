'''
task runner, @see https://www.pyinvoke.org/
'''

from invoke import task

@task(aliases=['startdb'])
def start_test_db(ctx):
    ctx.run('redis-server ./tests/redis-test.conf', pty=True)

@task(aliases=['stopdb'])
def stop_test_db(ctx):
    ctx.run('redis-cli -a testpw shutdown', pty=True)

@task
def run(ctx):
    ctx.run('poetry run uvicorn petnet_app.main:app --port 9001 --reload', pty=True)

@task
def test(ctx):
    ctx.run('/bin/rm -fr logs data')
    ctx.run('poetry run pytest --cov=petnet_app/ --cov-branch tests/', pty=True)

@task(aliases=['cov'])
def cover(ctx):
    ctx.run('poetry run coverage report -m', pty=True)
    ctx.run('poetry run coverage html --title="PetNetApp Test Coverage"', pty=True)

@task(aliases=['int'])
def integration(ctx):
    ctx.run('poetry run tests/integration-tests.py', pty=True)

@task(name='format', aliases=['black','isort'])
def formatter(ctx):
    ctx.run('black petnet_app/ tests/', pty=True)
    ctx.run('isort petnet_app/', pty=True)
    ctx.run('poetry run ruff check --fix ./petnet_app/', pty=True)

@task
def ruff(ctx):
    ctx.run('poetry run ruff check ./petnet_app/', pty=True)

@task
def lint(ctx):
    ctx.run('poetry run ruff check ./petnet_app/', pty=True)
    ctx.run('poetry run pylint ./petnet_app/', pty=True)

@task(aliases=['todo'])
def todos(ctx):
    ctx.run('rg TODO petnet_app/*.py tests/*.py', pty=True)

@task
def mypy(ctx):
    ctx.run('poetry run mypy petnet_app/', pty=True)

@task
def refurb(ctx):
    ctx.run('poetry run refurb petnet_app/ tests/', pty=True)

@task
def repl(ctx):
    ctx.run('poetry run bpython -i .repl-start.py', pty=True)

@task(aliases=['precommit'])
def pre(ctx):
    ctx.run('clear', pty=True)
    test(ctx)
    cover(ctx)
    formatter(ctx)
    lint(ctx)
    refurb(ctx)
    mypy(ctx)

