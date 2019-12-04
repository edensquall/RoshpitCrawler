from abc import abstractmethod

from ..models.item import Item
from ..models.item_type import ItemType
from ..models.property import Property
from ..repositories.base_item_repo import BaseItemRepo
from ..repositories.base_item_type_repo import BaseItemTypeRepo
from ..repositories.base_property_repo import BasePropertyRepo
from ..unit_of_works.base_uow import BaseUOW


class BaseCollectItemInfoService:

    def __init__(self, item_repo: BaseItemRepo, item_type_repo: BaseItemTypeRepo, property_repo: BasePropertyRepo,
                 uow: BaseUOW):
        raise NotImplementedError

    @abstractmethod
    def get_item_type_by_id(self, item_type: ItemType) -> ItemType:
        raise NotImplementedError

    @abstractmethod
    def add_new_item_type(self, item_type: ItemType) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_item_by_id(self, item: Item) -> Item:
        raise NotImplementedError

    @abstractmethod
    def add_new_item(self, item: Item) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_property_by_id(self, property: Property) -> Property:
        raise NotImplementedError

    @abstractmethod
    def add_new_property(self, property: Property) -> None:
        raise NotImplementedError
