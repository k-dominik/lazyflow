###############################################################################
#   lazyflow: data flow based lazy parallel computation framework
#
#       Copyright (C) 2011-2014, the ilastik developers
#                                <team@ilastik.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the Lesser GNU General Public License
# as published by the Free Software Foundation; either version 2.1
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# See the files LICENSE.lgpl2 and LICENSE.lgpl3 for full text of the
# GNU Lesser General Public License version 2.1 and 3 respectively.
# This information is also available on the ilastik web site at:
# 		   http://ilastik.org/license/
###############################################################################

import threading
import queue

import pytest

from lazyflow.request.threadPool import ThreadPool


@pytest.fixture
def pool():
    p = None
    try:
        p = ThreadPool(num_workers=4)
        yield p
    finally:
        if p:
            p.stop()


def test_basic(pool):
    f1_started = threading.Event()
    f2_started = threading.Event()
    f2_finished = threading.Event()

    def f1():
        f1_started.set()

    def f2():
        f2_started.set()
        f1_started.wait()
        f2_finished.set()

    pool.wake_up(f2)
    f2_started.wait()
    pool.wake_up(f1)

    f2_finished.wait()

    assert f1.assigned_worker != f2.assigned_worker


def test_callable_executes_in_same_thread(pool):
    func_finished = threading.Event()
    thread_ids = []

    def func():
        thread_ids.append(threading.current_thread().ident)
        func_finished.set()

    for _i in range(pool.num_workers):
        func_finished.clear()
        pool.wake_up(func)
        func_finished.wait()

    assert len(set(thread_ids)) == 1, "Callable has been executed in a different worker thread"


def test_generator_executes_in_same_thread(pool):
    gen_stepped = threading.Event()
    test_finished = threading.Event()
    thread_ids = []

    def make_gen():
        while True:
            thread_ids.append(threading.current_thread().ident)
            gen_stepped.set()
            yield

    class GenTask:
        def __init__(self, gen):
            self.gen = gen

        def __call__(self):
            return next(self.gen)

    gen_task = GenTask(make_gen())

    # Submit an infinite generator task and wait for it to be scheduled.
    # Now 1 worker is occupied with that task.
    pool.wake_up(gen_task)
    gen_stepped.wait()

    # Task with some ordering that just waits for an event.
    class WaitTask:
        def __init__(self, priority):
            self.priority = priority

        def __lt__(self, other):
            return self.priority < other.priority

        def __call__(self):
            test_finished.wait()

    # Now all workers are occupied, and 1 of these tasks is not scheduled yet.
    for i in range(pool.num_workers):
        pool.wake_up(WaitTask(i))

    # Force the generator task to take 1 more step.
    gen_stepped.clear()
    pool.wake_up(gen_task)
    gen_stepped.wait()

    # Ensure that both generator invocations have been executed in the same thread.
    assert len(thread_ids) == 2
    assert thread_ids[0] == thread_ids[1]

    # Release tasks that occupy workers, so that the thread pool can stop.
    test_finished.set()
