import logging
from threading import Timer, Lock
from time import sleep

logger = logging.getLogger('cron_helper')

class Periodic(object):
    """
    A periodic task running in threading.Timers
    """

    def __init__(self, interval, function, *args, **kwargs):
        self._lock = Lock()
        self._timer = None
        self.function = function
        self.interval = interval
        self.args = args
        self.kwargs = kwargs
        self._stopped = True
        if kwargs.pop('autostart', True):
            self.start()

    def start(self, from_run=False):
        self._lock.acquire()
        if from_run or self._stopped:
            self._stopped = False
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self._lock.release()

    def _run(self):
        self.start(from_run=True)
        self.function(*self.args, **self.kwargs)

    def stop(self):
        self._lock.acquire()
        self._stopped = True
        self._timer.cancel()
        self._lock.release()

if __name__ == "__main__":

    def doshit(asd):
        print("doshit" + asd)
    
    # a = Periodic()
    rt = Periodic(1, doshit, "World") # it auto-starts, no need of rt.start()
    try:
        sleep(5) # your long-running job goes here...
    finally:
        rt.stop() # better in a try/finally block to make sure the program ends!