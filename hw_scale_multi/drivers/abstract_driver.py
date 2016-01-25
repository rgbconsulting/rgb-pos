
import time
from threading import Thread, Lock
import logging

_logger = logging.getLogger(__name__)


class AbstractDriver(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        self.lock = Lock()
        self.scalelock = Lock()
        self.status = {'status': 'connecting', 'messages': []}
        self.weight = 0
        self.weight_info = 'ok'
        self.device = None
        self.weight_sleep = 1

    def lockedstart(self):
        with self.lock:
            if not self.isAlive():
                self.daemon = True
                self.start()

    def set_status(self, status, message=None):
        if status == self.status['status']:
            if message is not None and message != self.status['messages'][-1]:
                self.status['messages'].append(message)

                if status == 'error' and message:
                    _logger.error('Scale Error: '+message)
                elif status == 'disconnected' and message:
                    _logger.warning('Disconnected Scale: '+message)
        else:
            self.status['status'] = status
            if message:
                self.status['messages'] = [message]
            else:
                self.status['messages'] = []

            if status == 'error' and message:
                _logger.error('Scale Error: '+message)
            elif status == 'disconnected' and message:
                _logger.warning('Disconnected Scale: '+message)

    def get_device(self):
        pass

    def get_weight(self):
        self.lockedstart()
        self.weight_sleep = 0.2
        return self.weight

    def get_weight_info(self):
        self.lockedstart()
        return self.weight_info

    def get_status(self):
        self.lockedstart()
        return self.status

    def read_weight(self):
        pass

    def set_zero(self):
        pass

    def set_tare(self):
        pass

    def clear_tare(self):
        pass

    def run(self):
        self.device = None

        while self.running:
            if self.device:
                self.read_weight()
                time.sleep(self.weight_sleep)
                if self.weight_sleep < 1:
                    self.weight_sleep += 0.1
            else:
                with self.scalelock:
                    self.device = self.get_device()
                if not self.device:
                    time.sleep(5)

    def stop(self):
        self.running = False
        while self.isAlive():
            time.sleep(0.2)
            pass
