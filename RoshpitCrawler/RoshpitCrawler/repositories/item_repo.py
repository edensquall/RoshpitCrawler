from ..models import session
from ..models.item import Item
from ..repositories.base_item_repo import BaseItemRepo
from ..repositories.generic_repo import GenericRepo


class ItemRepo(GenericRepo[Item], BaseItemRepo):

    def get_by_item_name(self, item: Item) -> Item:
        return session.query(Item).filter_by(name=item.name).first()
