import unittest

import tests
from invoke import task
from tests.unittests import *


@task
def test(ctx):
    ctx.run('rq worker &')
    suite = unittest.TestLoader().loadTestsFromModule(tests)
    results = unittest.TextTestRunner(verbosity=2).run(suite)
    ctx.run('killall rq')

    if len(results.errors) > 0 or len(results.failures) > 0:
        exit(-1)
    else:
        exit(0)


@task
def deploy(ctx):
    ctx.run('ssh -o StrictHostKeyChecking=no -i ./travis_deploy/travis_ci.rsa '
            'ubuntu@52.3.221.80 "cd ReferenceLookupService && sh ./deploy.sh"')
