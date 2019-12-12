from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Type

T = TypeVar('T')


class BaseRepo(ABC, Generic[T]):

    @abstractmethod
    def get_all(self, model_class: Type[T]) -> List[T]:
        """
        取得某類別的所有資料
        Args:
            model_class: 某類別本身

        Returns: 某類別的所有資料

        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, model: T) -> T:
        """
        取得某類別符合此id的資料
        Args:
            model: 傳遞某類別參數

        Returns: 某類別符合此id的資料

        """
        raise NotImplementedError

    @abstractmethod
    def insert(self, model: T) -> None:
        """
        新增某類別的資料
        Args:
            model: 傳遞某類別參數

        Returns: None

        """
        raise NotImplementedError

    @abstractmethod
    def delete_all(self, model_class: Type[T]) -> None:
        """
        刪除某類別的所有資料
        Args:
            model_class: 某類別本身

        Returns: None

        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, model: T) -> None:
        """
        刪除某類別的資料
        Args:
            model: 傳遞某類別參數

        Returns: None

        """
        raise NotImplementedError
