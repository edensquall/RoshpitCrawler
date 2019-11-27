from ..models.item_type import ItemType
from ..repositories.base_item_type_repo import BaseItemTypeRepo
from ..repositories.generic_repo import GenericRepo


class ItemTypeRepo(GenericRepo[ItemType], BaseItemTypeRepo):
    pass
