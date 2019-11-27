from sqlalchemy.util.compat import contextmanager

from ..models import session
from ..unit_of_works.base_uow import BaseUOW


class SQLAlchemyUOW(BaseUOW):

    def complete(self):
        session.commit()

    def rollback(self):
        session.rollback()

    @contextmanager
    def auto_complete(self):
        try:
            yield
            self.complete()
        except Exception as e:
            self.rollback()
            raise e
