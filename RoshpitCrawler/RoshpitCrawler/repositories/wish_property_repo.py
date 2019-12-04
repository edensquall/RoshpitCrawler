from ..models.wish_property import WishProperty
from ..repositories.base_wish_property_repo import BaseWishPropertyRepo
from ..repositories.generic_repo import GenericRepo


class WishPropertyRepo(GenericRepo[WishProperty], BaseWishPropertyRepo):
    pass
