from abc import abstractmethod
from typing import List

from ..models.notify import Notify
from ..models.user import User
from ..models.wish import Wish
from ..repositories.base_item_repo import BaseItemRepo
from ..repositories.base_notify_repo import BaseNotifyRepo
from ..repositories.base_parameter_repo import BaseParameterRepo
from ..repositories.base_property_repo import BasePropertyRepo
from ..repositories.base_wish_repo import BaseWishRepo
from ..unit_of_works.base_uow import BaseUOW


class BaseCollectAuctionInfoService:

    def __init__(self, item_repo: BaseItemRepo, property_repo: BasePropertyRepo, wish_repo: BaseWishRepo,
                 notify_repo: BaseNotifyRepo, parameter_repo: BaseParameterRepo, uow: BaseUOW):
        raise NotImplementedError

    @abstractmethod
    def get_crawled_auction_id(self) -> str:
        """
        取得上次爬過的拍賣品id
        Returns: 上次爬過的拍賣品id

        """
        raise NotImplementedError

    @abstractmethod
    def set_crawled_auction_id(self, crawled_auction_id: str) -> None:
        """
        設定爬過的拍賣品id
        Returns: None

        """
        raise NotImplementedError

    @abstractmethod
    def find_potential_buyer(self, auction: Wish) -> List[User]:
        """
        尋找有這項拍賣品需求的買家
        Returns: 有這項拍賣品需求的買家

        """
        raise NotImplementedError

    @abstractmethod
    def delete_notify(self, notify: Notify) -> None:
        """
        移除通知
        Returns: None

        """
        raise NotImplementedError

    @abstractmethod
    def send_mail_notify(self, potential_buyer: User, auction: Wish, auction_id) -> None:
        """
        透過email送出通知
        Args:
            potential_buyer: 有這項拍賣品需求的買家
            auction: 拍賣品資訊
            auction_id: 拍賣品id

        Returns: None

        """
        raise NotImplementedError

    @abstractmethod
    def send_line_notify(self, potential_buyer: User, auction: Wish, auction_id) -> None:
        """
        透過line送出通知
        Args:
            potential_buyer: 有這項拍賣品需求的買家
            auction: 拍賣品資訊
            auction_id: 拍賣品id

        Returns: None

        """
        raise NotImplementedError

    @abstractmethod
    def notify_potential_buyer(self, auction: Wish, auction_id: str) -> None:
        """
        通知有這項拍賣品需求的買家
        Args:
            auction: 拍賣品資訊
            auction_id: 拍賣品id

        Returns: None

        """
        raise NotImplementedError
