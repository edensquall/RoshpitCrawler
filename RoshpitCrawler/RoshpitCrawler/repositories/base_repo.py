from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Type

T = TypeVar('T')


class BaseRepo(ABC, Generic[T]):

    @abstractmethod
    def get_all(self, model_class: Type[T]) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, model: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def insert(self, model: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_all(self, model_class: Type[T]) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, model: T) -> None:
        raise NotImplementedError
