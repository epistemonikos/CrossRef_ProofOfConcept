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
