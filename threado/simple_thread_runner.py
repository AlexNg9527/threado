import threading
import queue
from loguru import logger
from typing import Callable, Any, Iterator


class SimpleThreadsRunner:
    """
    A simple ThreadsRunner. This runs multiple threads to do the I/O;
    Performance is at least as good as Queue producer/consumer, which works in an analogous fashion.
    Empty the queue after use.
    """

    def __init__(self, num_workers: int, fn: Callable[..., Any]):
        self._queue = queue.Queue()
        self._lock = threading.RLock()
        self.num_workers = num_workers
        self._threads = []
        self.fn = fn

    def prepare_threads(self) -> None:
        """
        Threads are created only function is called, and terminate before it returns. They are there primarily to parallelize I/O (i.e.fetching web pages, download picture, scroll elasticsearch).
        """
        for i in range(self.num_workers):
            t = threading.Thread(target=self.fetch, args=(), name=f"child_thread_{i}")
            # t.setDaemon(True)
            t.start()
            self._threads.append(t)

    def wait_threads(self):
        """
        Tell all the threads to terminate (by sending a sentinel value) and
        wait for them to do so.
        """

        for t in self._threads:
            t.join()
        self._threads = []

    def fetch(self) -> None:
        """
        Get a Data to fetch from the work _queue.
        This is a handy method to run in a thread.
        """
        while True:
            try:
                _data = self._queue.get_nowait()
                i = self._queue.qsize()
            except Exception as e:
                print(e)
                break
            logger.info('Current Thread Name Running %s ...' % threading.currentThread().name)
            self.fn(_data)
            self._queue.task_done()
            logger.info(f"Tasks left:{i}")

    def q_producer(self, _data):
        self._queue.put(_data)

    def get_qsize(self) -> int:
        """Get current size of queue, be aware this value is changed frequently
        as multiple threads may produce/consume data to the queue"""
        return self._queue.qsize()

    def q_consumer(self):
        """
        This fn can be used separated with q_producer
        Example:
            for _ in iter_data:
                sr.q_producer(_)
            sr.q_consumer()
        """
        with self._lock:
            try:
                self.prepare_threads()
            finally:
                self.wait_threads()

    def run_threads(self, iter_data: Iterator[Any], batch_size: int = None):
        """Add batch_size params in case iter_data is huge number"""
        for _ in iter_data:
            self.q_producer(_)
            if batch_size:
                _qsize = self.get_qsize()
                if _qsize >= batch_size:
                    self.q_consumer()

        _qsize = self.get_qsize()
        if _qsize != 0:
            self.q_consumer()
