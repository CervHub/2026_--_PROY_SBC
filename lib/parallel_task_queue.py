import threading
import queue
from concurrent.futures import Future

class ParallelTaskQueue:
    _task_queue = queue.Queue()
    _workers = []
    _initialized = False
    _max_workers = 8

    @staticmethod
    def _worker():
        while True:
            func, args, kwargs, future = ParallelTaskQueue._task_queue.get()
            try:
                result = func(*args, **kwargs)
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)
            finally:
                ParallelTaskQueue._task_queue.task_done()

    @staticmethod
    def _init_workers():
        if not ParallelTaskQueue._initialized:
            for _ in range(ParallelTaskQueue._max_workers):
                t = threading.Thread(target=ParallelTaskQueue._worker, daemon=True)
                t.start()
                ParallelTaskQueue._workers.append(t)
            ParallelTaskQueue._initialized = True

    @staticmethod
    def submit(func, *args, **kwargs):
        ParallelTaskQueue._init_workers()
        future = Future()
        ParallelTaskQueue._task_queue.put((func, args, kwargs, future))
        return future