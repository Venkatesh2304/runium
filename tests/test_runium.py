import pytest
import time
import timeit
from runium.core import Runium


@pytest.fixture(scope="module")
def rnt():
    return Runium()


@pytest.fixture(scope="module")
def rnp():
    return Runium(mode='multiprocessing')


class TestTimes():
    def test_threading(self, rnt):
        rt = rnt.new_task(runnium_param).run(times=3).result()
        assert rt['iterations'] == 3

    def test_processing(self, rnp):
        rp = rnp.new_task(runnium_param).run(times=3).result()
        assert rp['iterations'] == 3


class TestLoopDrift():
    def test_threading(selft, rnt):
        prev_time = time.time()
        rnt.new_task(simple_task).run(every=0.1, times=10).result()
        time_elapsed = time.time() - prev_time
        is_ok = (time_elapsed < 1) and (time_elapsed > 0.88)
        assert is_ok is True

    def test_processing(selft, rnp):
        prev_time = time.time()
        rnp.new_task(simple_task).run(every=0.1, times=10).result()
        time_elapsed = time.time() - prev_time
        is_ok = (time_elapsed < 1) and (time_elapsed > 0.88)
        assert is_ok is True


class TestStartIn():
    def test_threading(self, rnt):
        prev_time = time.time()
        rnt.new_task(simple_task).run(start_in=0.1).result()
        time_elapsed = time.time() - prev_time
        is_ok = (time_elapsed < 0.11) and (time_elapsed > 0.09)
        assert is_ok is True

    def test_processing(self, rnp):
        """
        start_in : int , the number of seconds to delay the start of function 
        The test it to check the time taken to end the asyc function is between 0.9 and 0.11 s , 
        Given the start_in is 0.1 for that function . 
        Problem in flaky test : 
        It uses time.time() which is not accurate when calculating such timings of 0.01 seconds and 
        also running the task one time to calculate time is quite varying . 
        So , we will use timeit.repeat to get the time for running the test n times with atleast 
        k success . 
        I have tuned the parameters to n = 10 and k = 8 .
        """
        n = 10 
        k = 8
        timings = timeit.repeat(lambda : rnp.new_task(simple_task).run(start_in=0.1).result() , number = 1,repeat = n)
        succesfull_timings = list(filter(lambda time : time < 0.11 and time > 0.09 , timings))
        is_ok = len(succesfull_timings) >= k 
        assert is_ok is True 



class TestTaskSkipping():
    def test_threading(self, rnt):
        prev_time = time.time()
        rnt.new_task(sleepy_task).run(every=0.1, times=2).result()
        time_elapsed = time.time() - prev_time
        is_ok = (time_elapsed < 0.51) and (time_elapsed > 0.2)
        assert is_ok is True

    def test_processing(self, rnp):
        prev_time = time.time()
        rnp.new_task(sleepy_task).run(every=0.1, times=2).result()
        time_elapsed = time.time() - prev_time
        is_ok = (time_elapsed < 0.51) and (time_elapsed > 0.2)
        assert is_ok is True


class TestKwargs():
    def test_threading(self, rnt):
        r = rnt.new_task(
            task_with_kwargs, kwargs={'msg': 'Spam, Spam, Spam, egg and Spam'}
        ).run().result()
        assert r == 'Spam, Spam, Spam, egg and Spam'

    def test_processing(self, rnp):
        r = rnp.new_task(
            task_with_kwargs, kwargs={'msg': 'Spam, Spam, Spam, egg and Spam'}
        ).run().result()
        assert r == 'Spam, Spam, Spam, egg and Spam'


class TestReturnException():
    def test_threading(self, rnt):
        r = rnt.new_task(task_with_exception).run().result()
        assert type(r).__name__ == 'ValueError'

    def test_processing(self, rnp):
        r = rnp.new_task(task_with_exception).run().result()
        assert type(r).__name__ == 'ValueError'


class TestKwargsBleeding():
    def test_threading(self, rnt):
        assert rnt.new_task(simple_task).run().result() is True

    def test_processing(self, rnp):
        assert rnp.new_task(simple_task).run().result() is True


class TestCallbacks(object):
    def test_on_finished_success_threading(self, rnt):
        assert rnt.new_task(task_callback_success).on_finished(
            se_callback, updates_result=True
        ).run().result() == 'Success'

    def test_on_finished_success_processing(self, rnp):
        assert rnp.new_task(task_callback_success).on_finished(
            se_callback, updates_result=True
        ).run().result() == 'Success'

    def test_on_finished_error_threading(self, rnt):
        assert rnt.new_task(task_callback_error).on_finished(
            se_callback, updates_result=True
        ).run().result() == 'Error'

    def test_on_finished_error_processing(self, rnp):
        assert rnp.new_task(task_callback_error).on_finished(
            se_callback, updates_result=True
        ).run().result() == 'Error'

    def test_on_success_threading(self, rnt):
        assert rnt.new_task(task_callback_success).on_success(
            success_callback, updates_result=True
        ).run().result() == 'Success'

    def test_on_success_processing(self, rnp):
        assert rnp.new_task(task_callback_success).on_success(
            success_callback, updates_result=True
        ).run().result() == 'Success'

    def test_on_error_threading(self, rnt):
        assert rnt.new_task(task_callback_error).on_error(
            error_callback, updates_result=True
        ).run().result() == 'Error'

    def test_on_error_processing(self, rnp):
        assert rnp.new_task(task_callback_error).on_error(
            error_callback, updates_result=True
        ).run().result() == 'Error'

    def test_on_iter_success_threading(self, rnt):
        assert rnt.new_task(task_callback_success).on_iter(
            se_callback, updates_result=True
        ).run(times=3).result() == 'Success'

    def test_on_iter_success_processing(self, rnp):
        assert rnp.new_task(task_callback_success).on_iter(
            se_callback, updates_result=True
        ).run(times=3).result() == 'Success'

    def test_on_iter_error_threading(self, rnt):
        assert rnt.new_task(task_callback_error).on_iter(
            se_callback, updates_result=True
        ).run(times=3).result() == 'Error'

    def test_on_iter_error_processing(self, rnp):
        assert rnp.new_task(task_callback_error).on_iter(
            se_callback, updates_result=True
        ).run(times=3).result() == 'Error'


class TestTasksList(object):
    def test_count_threading(self, rnt):
        r1 = rnt.new_task(simple_task)
        tasks_prev_count = len(rnt.pending_tasks())
        r1.run().result()
        assert tasks_prev_count == 1

    def test_count_finished_threading(self, rnt):
        rnt.new_task(simple_task).run().result()
        assert len(rnt.pending_tasks()) == 0

    def test_count_processing(self, rnp):
        r1 = rnp.new_task(simple_task)
        tasks_prev_count = len(rnp.pending_tasks())
        r1.run().result()
        assert tasks_prev_count == 1

    def test_count_finished_processing(self, rnp):
        rnp.new_task(simple_task).run().result()
        assert len(rnp.pending_tasks()) == 0


# DUMMY TASKS =================================================================
def simple_task():
    return True


def task_with_kwargs(msg=None, **kwargs):
    return msg


def runnium_param(runium):
    return runium


def task_with_exception(runium):
    raise ValueError('ni')
    return runium


def sleepy_task():
    time.sleep(0.2)
    return True


def task_callback_success():
    return 'Callback not fired.'


def task_callback_error():
    raise Exception('Callback not fired.')


def success_callback(success):
    if success:
        return 'Success'
    return None


def error_callback(error):
    if error:
        return 'Error'
    return None


def se_callback(success, error):
    if success:
        return 'Success'
    elif error:
        return 'Error'
    return None
