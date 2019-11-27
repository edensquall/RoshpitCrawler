from abc import abstractmethod

from ..models.property import Property
from ..repositories.base_repo import BaseRepo


class BasePropertyRepo(BaseRepo[Property]):

    @abstractmethod
    def get_by_name_type_item_id(self, property: Property) -> Property:
        raise NotImplementedError
        pass
