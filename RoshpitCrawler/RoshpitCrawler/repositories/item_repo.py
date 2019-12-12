from ..models.item import Item
from ..repositories.base_item_repo import BaseItemRepo
from ..repositories.generic_repo import GenericRepo


class ItemRepo(GenericRepo[Item], BaseItemRepo):
    pass
