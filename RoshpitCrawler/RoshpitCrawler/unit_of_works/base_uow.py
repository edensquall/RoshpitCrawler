from abc import ABC, abstractmethod

from sqlalchemy.util.compat import contextmanager


class BaseUOW(ABC):

    @abstractmethod
    def complete(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abstractmethod
    @contextmanager
    def auto_complete(self):
        raise NotImplementedError
