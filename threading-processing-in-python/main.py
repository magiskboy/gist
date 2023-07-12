import threading
import multiprocessing
import time
import requests

def measure(func):
    def f(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        print(f"{func.__name__} takes {time.time()-start} seconds")
        return ret

    return f


def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


@measure
def cpu_bounded_in_multiple_process():
    p1 = multiprocessing.Process(target=fib, args=(40,), daemon=True)
    p2 = multiprocessing.Process(target=fib, args=(40,), daemon=True)
    p1.start()
    p2.start()
    p1.join()
    p2.join()


@measure
def cpu_bounded_in_multiple_thread():
    t1 = threading.Thread(target=fib, args=(40,), daemon=True)
    t2 = threading.Thread(target=fib, args=(40,), daemon=True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


@measure
def cpu_bounded_in_single_thread():
    fib(40)
    fib(40)


@measure
def io_bounded_in_single_thread(n_iters=10):
    for i in range(n_iters):
        requests.get("https://api.github.com/users/magiskboy")


@measure
def io_bounded_in_multiple_threads(n_iters=10):
    ts = []
    for i in range(n_iters):
        t = threading.Thread(
            target=requests.get,
            kwargs={"url": "https://api.github.com/users/magiskboy"},
            daemon=True,
        )
        t.start()
        ts.append(t)

    for t in ts:
        t.join()


if __name__ == "__main__":
    cpu_bounded_in_single_thread()
    cpu_bounded_in_multiple_thread()
    cpu_bounded_in_multiple_process()
    io_bounded_in_single_thread()
    io_bounded_in_multiple_threads()
