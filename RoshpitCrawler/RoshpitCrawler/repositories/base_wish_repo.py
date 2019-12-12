from abc import abstractmethod
from typing import List

from ..models.wish import Wish
from ..repositories.base_repo import BaseRepo


class BaseWishRepo(BaseRepo[Wish]):

    @abstractmethod
    def get_satisfiable_wishes(self, wish: Wish) -> List[Wish]:
        """
        取得與拍賣品數值相符的wish
        Args:
            wish: 拍賣品的數值

        Returns: 與拍賣品數值相符的wish

        """
        raise NotImplementedError
