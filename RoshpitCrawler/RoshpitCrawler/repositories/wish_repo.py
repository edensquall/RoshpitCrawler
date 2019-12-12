from typing import List

from sqlalchemy import or_, and_

from ..models import session
from ..models.item import Item
from ..models.property import Property
from ..models.user import User
from ..models.wish import Wish
from ..models.wish_property import WishProperty
from ..repositories.base_wish_repo import BaseWishRepo
from ..repositories.generic_repo import GenericRepo


class WishRepo(GenericRepo[Wish], BaseWishRepo):

    def get_satisfiable_wishes(self, wish: Wish) -> List[Wish]:
        """
        取得與拍賣品數值相符的wish
        Args:
            wish: 拍賣品的數值

        Returns: 與拍賣品數值相符的wish

        """
        query = session \
            .query(Wish) \
            .join(Item) \
            .join(Property) \
            .join(User) \
            .outerjoin(WishProperty, WishProperty.property_id == Property.id). \
            filter(Wish.item_id == wish.item_id). \
            filter(Wish.currency == wish.currency). \
            filter(or_(Wish.min_level == 0, wish.min_level == 0, Wish.min_level <= wish.min_level)). \
            filter(or_(Wish.max_bid == 0, wish.max_bid == 0, Wish.max_bid >= wish.max_bid)). \
            filter(or_(Wish.max_buyout == 0, wish.max_buyout == 0, Wish.max_buyout >= wish.max_buyout)). \
            filter(or_(*[(and_(Property.id == wish_property.property_id,
                               or_(WishProperty.property_id == None,
                                   and_(WishProperty.property_id == wish_property.property_id,
                                        or_(WishProperty.roll == None, WishProperty.roll <= wish_property.roll))))
                          for wish_property in wish.wish_properties)]))

        result = query.all()
        return result
