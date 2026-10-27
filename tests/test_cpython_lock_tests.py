#!/usr/bin/env python3

_license = """
blanket
Copyright 2025-2026 Larry Hastings
All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import blankettestlib
blankettestlib.preload_local_blanket()

import unittest

from blanket import Scenario

try:
    from test import lock_tests
except ModuleNotFoundError as e:
    if e.name not in ("test", "test.lock_tests"):
        raise
    lock_tests = None


if lock_tests is None:
    class TestCPythonLockTestsUnavailable(unittest.TestCase):
        @unittest.skip("CPython's test.lock_tests suite is not installed")
        def test_cpython_lock_tests(self):
            pass
else:
    class TestCPythonLockTestsLock(lock_tests.LockTests):
        locktype = staticmethod(lambda: Scenario().Lock())

    class TestCPythonLockTestsRLock(lock_tests.RLockTests):
        locktype = staticmethod(lambda: Scenario().RLock())

    class TestCPythonLockTestsCondition(lock_tests.ConditionTests):
        condtype = staticmethod(lambda lock=None: Scenario().Condition(lock))

    class TestCPythonLockTestsSemaphore(lock_tests.SemaphoreTests):
        semtype = staticmethod(lambda value=1: Scenario().Semaphore(value))

    class TestCPythonLockTestsBoundedSemaphore(lock_tests.BoundedSemaphoreTests):
        semtype = staticmethod(lambda value=1: Scenario().BoundedSemaphore(value))

    class TestCPythonLockTestsEvent(lock_tests.EventTests):
        eventtype = staticmethod(lambda: Scenario().Event())

    class TestCPythonLockTestsBarrier(lock_tests.BarrierTests):
        barriertype = staticmethod(
            lambda parties, action=None, timeout=None:
                Scenario().Barrier(parties, action, timeout)
        )


def run_tests():
    blankettestlib.run(name="CPython lock tests", module=__name__)


if __name__ == '__main__':
    run_tests()
    blankettestlib.finish()
