from ..models import session
from ..models.property import Property
from ..repositories.base_property_repo import BasePropertyRepo
from ..repositories.generic_repo import GenericRepo


class PropertyRepo(GenericRepo[Property], BasePropertyRepo):

    def get_by_name_type_item_id(self, property: Property) -> Property:
        return session.query(Property).filter_by(name=property.name, type=property.type,
                                                 item_id=property.item_id).first()
