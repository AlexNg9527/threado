import threading
import queue
from loguru import logger
from typing import Callable, Any, Iterator, Iterable


class SimpleThreadsRunner:
    """
    A simple ThreadsRunner. This runs multiple threads to do the I/O;
    Performance is at least as good as Queue producer/consumer, which works in an analogous fashion.
    Empty the queue after use.
    """
    SENTINEL = object()

    def __init__(self):
        self._queue = queue.Queue()
        self._lock = threading.RLock()
        self._threads = []

    def prepare_threads(self, num_workers: int, fn: Callable[..., Any]) -> None:
        """
        Threads are created only function is called, and terminate before it returns.
        They are there primarily to parallelize I/O
        (i.e.fetching web pages, download picture, scroll elasticsearch).
        """
        for i in range(num_workers):
            t = threading.Thread(target=self.fetch, args=(fn,), name=f"child_thread_{i}")
            t.setDaemon(True)
            t.start()
            self._threads.append(t)

    def wait_threads(self):
        """
        Tell all the threads to terminate (by sending a sentinel value) and
        wait for them to do so.
        """
        # Note that you need two loops, since you can't say which
        # thread will get each sentinel
        for _ in self._threads:
            self._queue.put(self.SENTINEL)  # sentinel
        for t in self._threads:
            t.join()
        self._threads = []

    def fetch(self, fn: Callable[..., Any]) -> None:
        """
        Get a Data to fetch from the work _queue.
        This is a handy method to run in a thread.
        """
        while True:
            try:
                _data: Iterable = self._queue.get_nowait()
                i = self._queue.qsize()
            except Exception as e:
                logger.error(e)
                break
            logger.info('Current Thread Name Running %s ...' % threading.currentThread().name)
            try:
                if _data is self.SENTINEL:
                    return
                fn(_data)
            except Exception as e:
                raise f'function: {fn.__name__} execution: {e}'
            self._queue.task_done()
            logger.info(f"Tasks left:{i}")

    def q_producer(self, _data):
        self._queue.put(_data)

    def get_qsize(self) -> int:
        """Get current size of queue, be aware this value is changed frequently
        as multiple threads may produce/consume data to the queue"""
        return self._queue.qsize()

    def q_consumer(self, num_workers: int, fn: Callable[..., Any]):
        """
        Function can be used separately with q_producer
        """
        with self._lock:
            try:
                self.prepare_threads(num_workers, fn)
            finally:
                self.wait_threads()

    def run_threads(self, num_workers: int, fn: Callable[..., Any], iter_data: Iterator[Any], batch_size: int = None):
        """Add batch_size params in case iter_data is huge number"""
        for _ in iter_data:
            self.q_producer(_)
            if batch_size:
                _qsize = self.get_qsize()
                if _qsize >= batch_size:
                    self.q_consumer(num_workers, fn)

        _qsize = self.get_qsize()
        if _qsize != 0:
            self.q_consumer(num_workers, fn)
