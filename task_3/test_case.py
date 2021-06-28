import logging
import os
import time
from abc import ABC, abstractmethod
from os.path import expanduser

import psutil as psutil

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
LOG.propagate = False
LOG_FORMATTER = logging.Formatter(
    "%(asctime)s %(filename)s: %(levelname)s %(message)s")
FILE_LOGGING_HANDLER = logging.FileHandler('log_file.log', encoding="UTF-8")
FILE_LOGGING_HANDLER.setFormatter(LOG_FORMATTER)
LOG.addHandler(FILE_LOGGING_HANDLER)


class PrepareUnixTimeException(Exception):
    """Ошибка при нечетности времени."""
    pass


class PrepareMemoryException(Exception):
    """Ошибка при малом объеме памяти."""
    pass


class TestBase(ABC):
    """Тест кейс базовый."""

    def __init__(self, tc_id: int, name: str):
        self.tc_id = tc_id
        self.name = name
        LOG.info(f'TestCase {self.tc_id}, {self.name} is created')

    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def clean_up(self):
        pass

    def execute(self):
        try:
            self.prepare()
            self.run()
            self.clean_up()
        except BaseException as e:
            LOG.info(
                (f'TestCase {self.tc_id}, {self.name} '
                 f'is created, exception: {e}')
            )


class TestCase1(TestBase):
    """Тест кейс 1."""

    def __init__(self, tc_id: int, name: str):
        super().__init__(tc_id, name)

    def prepare(self):
        time_now = int(time.time())
        LOG.info(
            (f'TestCase: id - {self.tc_id}, name - {self.name} '
             f'is checking time {time_now}')
        )
        if time_now % 2 != 0:
            raise PrepareUnixTimeException(
                f'Prepare failed - {time_now} odd number!'
            )

    def run(self):
        home_dir = expanduser("~")
        LOG.info(
            (f'TestCase: id - {self.tc_id}, name - {self.name} '
             f'is checking dir {home_dir}, files {os.listdir(home_dir)}')
        )
        for file in os.listdir(home_dir):
            print(file)

    def clean_up(self):
        pass


class TestCase2(TestBase):
    """Тест кейс 2."""

    def __init__(self, tc_id: int, name: str):
        super().__init__(tc_id, name)
        self.random_file = None

    def prepare(self):
        memory = psutil.virtual_memory()
        memory_gb = int(memory.total / 1024 ** 3)
        LOG.info(
            (f'TestCase: id - {self.tc_id}, '
             f'name - {self.name} is checking memory {memory_gb}Gb')
        )
        if memory_gb < 1:
            raise PrepareMemoryException(
                f'Prepare failed: PHYSICAL MEMORY {memory_gb} < 1'
            )

    def run(self, file_name='test', size=1024000):
        LOG.info(
            (f'TestCase: id - {self.tc_id}, name - {self.name}'
             f' is writing {size} bytes to file {file_name}')
        )
        self.random_file = file_name
        with open(self.random_file, 'wb') as file:
            file.write(os.urandom(size))

    def clean_up(self):
        LOG.info(
            f'TestCase: id - {self.tc_id}, name - {self.name} is cleaning')
        os.remove(self.random_file)


def main():
    case_1 = TestCase1(tc_id=1, name='TestCase1')
    case_1.execute()
    case_2 = TestCase2(tc_id=2, name='TestCase2')
    case_2.execute()


if __name__ == '__main__':
    main()
