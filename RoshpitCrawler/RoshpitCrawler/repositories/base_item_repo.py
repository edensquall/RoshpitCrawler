from abc import abstractmethod

from ..models.item import Item
from ..repositories.base_repo import BaseRepo


class BaseItemRepo(BaseRepo[Item]):

    @abstractmethod
    def get_by_item_name(self, item: Item) -> Item:
        raise NotImplementedError
    pass
