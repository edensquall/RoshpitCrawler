from injector import inject

from ..models.item import Item
from ..models.item_type import ItemType
from ..models.property import Property
from ..repositories.base_item_repo import BaseItemRepo
from ..repositories.base_item_type_repo import BaseItemTypeRepo
from ..repositories.base_property_repo import BasePropertyRepo
from ..services.base_collect_item_info_service import BaseCollectItemInfoService
from ..unit_of_works.base_uow import BaseUOW


class CollectItemInfoService(BaseCollectItemInfoService):

    @inject
    def __init__(self, item_repo: BaseItemRepo, item_type_repo: BaseItemTypeRepo, property_repo: BasePropertyRepo,
                 uow: BaseUOW):
        self.item_repo = item_repo
        self.item_type_repo = item_type_repo
        self.property_repo = property_repo
        self.uow = uow

    def get_item_type_by_id(self, item_type: ItemType) -> ItemType:
        return self.item_type_repo.get_by_id(item_type)

    def add_new_item_type(self, item_type: ItemType) -> None:
        with self.uow.auto_complete():
            self.item_type_repo.insert(item_type)

    def delete_all_item_type(self) -> None:
        with self.uow.auto_complete():
            self.item_type_repo.delete_all(ItemType)

    def get_item_by_id(self, item: Item) -> Item:
        return self.item_repo.get_by_id(item)

    def add_new_item(self, item: Item) -> None:
        with self.uow.auto_complete():
            self.item_repo.insert(item)

    def delete_all_item(self) -> None:
        with self.uow.auto_complete():
            self.item_repo.delete_all(Item)

    def get_property_by_id(self, property: Property) -> Property:
        return self.property_repo.get_by_id(property)

    def add_new_property(self, property: Property) -> None:
        with self.uow.auto_complete():
            self.property_repo.insert(property)

    def delete_all_property(self) -> None:
        with self.uow.auto_complete():
            self.property_repo.delete_all(Property)
