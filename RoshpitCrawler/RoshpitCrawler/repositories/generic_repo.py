from typing import List, TypeVar, Type

from ..models import session
from ..repositories.base_repo import BaseRepo

T = TypeVar('T')


class GenericRepo(BaseRepo[T]):

    def get_all(self, model_class: Type[T]) -> List[T]:
        return session.query(model_class).all()

    def get_by_id(self, model: T) -> T:
        return session.query(type(model)).filter_by(id=model.id).first()

    def insert(self, model: T) -> None:
        session.merge(model)
        session.flush()

    def delete_all(self, model_class: Type[T]) -> None:
        session.execute('SET FOREIGN_KEY_CHECKS = 0')
        session.query(model_class).delete()
        session.execute('SET FOREIGN_KEY_CHECKS = 1')

    def delete(self, model: T) -> None:
        session.query(type(model)).filter_by(id=model.id).delete()
