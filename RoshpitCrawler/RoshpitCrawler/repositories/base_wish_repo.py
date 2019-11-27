from abc import abstractmethod
from typing import List

from ..models.wish import Wish
from ..repositories.base_repo import BaseRepo


class BaseWishRepo(BaseRepo[Wish]):

    @abstractmethod
    def get_satisfiable_wishes(self, wish: Wish) -> List[Wish]:
        raise NotImplementedError
