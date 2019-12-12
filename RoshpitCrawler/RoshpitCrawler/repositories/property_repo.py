from ..models.property import Property
from ..repositories.base_property_repo import BasePropertyRepo
from ..repositories.generic_repo import GenericRepo


class PropertyRepo(GenericRepo[Property], BasePropertyRepo):
    pass
