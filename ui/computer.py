import signal
from pexpect.popen_spawn import PopenSpawn
from init import EXE_PATH


class Computer:
    """
    This class represents the computer player.
    """

    __slots__ = ('_process', '_executable')

    def __init__(self):
        self._executable = EXE_PATH
        self._process = None

    @property
    def process(self):
        return self._process

    @process.setter
    def process(self, value):
        self._process = value

    @property
    def executable(self):
        return self._executable

    def start(self):
        if self.process:
            self.stop()
        self.process = PopenSpawn(self.executable)
        print('Started process', self.process)

    def stop(self):
        if self.process:
            print('Stopped process', self.process)
            self.process.kill(signal.SIGKILL)
            self.process = None

    def pause(self):
        if self.process:
            self.process.kill(signal.SIGSTOP)

    def resume(self):
        if self.process:
            self.process.kill(signal.SIGCONT)

    def read_buffer(self):
        if self.process:
            return self.process.before.decode('utf-8').split('\n')

    def next_move(self):
        if self.process:
            buffer = self.read_buffer()
            if buffer:
                coordinates = [int(i) for i in buffer[-1].split()]
                return coordinates
            return None
