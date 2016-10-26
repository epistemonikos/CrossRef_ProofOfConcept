import unittest

import tests
from invoke import task
from tests.unittests import *


@task
def test(ctx):
    ctx.run('rq worker &')
    suite = unittest.TestLoader().loadTestsFromModule(tests)
    unittest.TextTestRunner(verbosity=2).run(suite)
    ctx.run('killall rq')
