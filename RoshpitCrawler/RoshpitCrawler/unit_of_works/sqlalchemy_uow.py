from sqlalchemy.util.compat import contextmanager

from ..models import session
from ..unit_of_works.base_uow import BaseUOW


class SQLAlchemyUOW(BaseUOW):

    def complete(self) -> None:
        """
        完成後正式修改資料
        Returns: None

        """
        session.commit()

    def rollback(self) -> None:
        """
        回復資料
        Returns: None

        """
        session.rollback()

    @contextmanager
    def auto_complete(self) -> None:
        """
        自動完成資料的修改
        無錯誤 -> 正式修改資料
        有錯誤 -> 回復資料
        Returns: None

        """
        try:
            yield
            self.complete()
        except Exception as e:
            self.rollback()
            raise e
