from typing import List, TypeVar, Type

from ..models import session
from ..repositories.base_repo import BaseRepo

T = TypeVar('T')


class GenericRepo(BaseRepo[T]):

    def get_all(self, model_class: Type[T]) -> List[T]:
        """
        取得某類別的所有資料
        Args:
            model_class: 某類別本身

        Returns: 某類別的所有資料

        """
        return session.query(model_class).all()

    def get_by_id(self, model: T) -> T:
        """
        取得某類別符合此id的資料
        Args:
            model: 傳遞某類別參數

        Returns: 某類別符合此id的資料

        """
        return session.query(type(model)).filter_by(id=model.id).first()

    def insert(self, model: T) -> None:
        """
        新增某類別的資料
        Args:
            model: 傳遞某類別參數

        Returns: None

        """
        session.merge(model)
        session.flush()

    def delete_all(self, model_class: Type[T]) -> None:
        """
        刪除某類別的所有資料
        Args:
            model_class: 某類別本身

        Returns: None

        """
        session.execute('SET FOREIGN_KEY_CHECKS = 0')
        session.query(model_class).delete()
        session.execute('SET FOREIGN_KEY_CHECKS = 1')

    def delete(self, model: T) -> None:
        """
        刪除某類別的資料
        Args:
            model: 傳遞某類別參數

        Returns: None

        """
        session.query(type(model)).filter_by(id=model.id).delete()
