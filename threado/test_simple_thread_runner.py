import queue
from unittest import TestCase
import time
import string

from simple_thread_runner import SimpleThreadsRunner


class TestSimpleThreadsRunner(TestCase):
    actions = list(string.ascii_lowercase)

    @staticmethod
    def n_print(n):
        print(n)
        time.sleep(1)

    def test_01_run_threads(self):
        sr = SimpleThreadsRunner()
        # LifoQueue
        sr._queue = queue.LifoQueue()
        sr.run_threads(5, fn=self.n_print, iter_data=self.actions)

    def test_02_batch_run_threads(self):
        sr = SimpleThreadsRunner()
        sr.run_threads(5, fn=self.n_print, iter_data=self.actions, batch_size=10)
