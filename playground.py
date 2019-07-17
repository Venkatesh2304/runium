import random
import time
from runium.core import Runium

some_data = 0


def add():
    time.sleep(0.5)
    global some_data
    print('Adding')
    some_data += 1
    return some_data


def simple_task():
    print('==> Simple task running.')
    return True


def a_callback(future):
    time.sleep(0.5)
    print('==> Callback called.')
    print('==> Exception:')
    print(future.exception())
    print('==> Result:')
    print(future.result())


def b_callback(future):
    print('==> b_callback initiated.')
    if future.exception():
        print('==> The task has failed.')
        print('==> Exception:')
        # print(future.result())
        print(future.exception())
    else:
        print('==> The task was successful.')
        print(future.result())


def task_time():
    sleep_for = random.uniform(0.1, 0.9)
    print(time.time(), ' --sleeping for:', sleep_for)
    time.sleep(sleep_for)


def task_args(msg, **kwargs):
    print('==>', msg, 'Running')
    time.sleep(1)
    print('==>', msg, 'Finished')
    return "task_args return msg: {}".format(msg)


def task_stats(runium, **kwargs):
    print(runium['iterations'], runium['iterations_remaining'])
    return runium


def t_exep():
    raise Exception('This is a test exception.')


if __name__ == "__main__":
    rnp = Runium(mode="multiprocessing")
    rnt = Runium()

    rnt.run(simple_task, times=10).result()
    rnt.run(simple_task).result()
    rnt.run(task_stats).result()
    rnt.run(simple_task, every='1 second', times=5, start_in=1).result()
    rnt.run(simple_task).result()
    rnt.run(task_args, kwargs={'msg': 'yo'}).result()
    rnt.run(simple_task)
