import datetime
import json
import os
import urllib
from typing import List

from ..models.notify import Notify
from ..models.parameter import Parameter
from ..models.user import User
from ..models.wish import Wish
from ..repositories.base_item_repo import BaseItemRepo
from ..repositories.base_notify_repo import BaseNotifyRepo
from ..repositories.base_parameter_repo import BaseParameterRepo
from ..repositories.base_property_repo import BasePropertyRepo
from ..repositories.base_wish_repo import BaseWishRepo
from ..services.base_collect_auction_info_service import BaseCollectAuctionInfoService
from ..unit_of_works.base_uow import BaseUOW
from ..utils.mailer import Mailer


class CollectAuctionInfoService(BaseCollectAuctionInfoService):

    def __init__(self, item_repo: BaseItemRepo, property_repo: BasePropertyRepo, wish_repo: BaseWishRepo,
                 notify_repo: BaseNotifyRepo, parameter_repo: BaseParameterRepo, uow: BaseUOW):
        self.item_repo = item_repo
        self.property_repo = property_repo
        self.wish_repo = wish_repo
        self.notify_repo = notify_repo
        self.parameter_repo = parameter_repo

        self.uow = uow

        self.mailer = Mailer()

    def get_is_spider_crawling(self) -> bool:
        """
        取得爬蟲是否在工作
        Returns: 爬蟲是否在工作

        """
        parameter = self.parameter_repo.get_by_id(Parameter(id='is_spider_crawling'))

        if parameter:
            return int(parameter.value) == 1
        else:
            return False

    def set_is_spider_crawling(self, is_spider_crawling: bool) -> None:
        """
        設定爬蟲是否在工作
        Returns: None

        """
        with self.uow.auto_complete():
            self.parameter_repo.insert(Parameter(id='is_spider_crawling', value="1" if is_spider_crawling else "0",
                                                 create_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                 modify_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def get_crawled_auction_id(self) -> int:
        """
        取得上次爬過的拍賣品id
        Returns: 上次爬過的拍賣品id

        """
        parameter = self.parameter_repo.get_by_id(Parameter(id='crawled_auction_id'))

        if parameter:
            return int(parameter.value)
        else:
            return 0

    def set_crawled_auction_id(self, crawled_auction_id: int) -> None:
        """
        設定爬過的拍賣品id
        Returns: None

        """
        with self.uow.auto_complete():
            self.parameter_repo.insert(Parameter(id='crawled_auction_id', value=str(crawled_auction_id),
                                                 create_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                 modify_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def find_potential_buyer(self, auction: Wish) -> List[User]:
        """
        尋找有這項拍賣品需求的買家
        Returns: 有這項拍賣品需求的買家

        """
        satisfiable_wishes = self.wish_repo.get_satisfiable_wishes(auction)
        return [wish.user for wish in satisfiable_wishes]

    def delete_notify(self, notify: Notify) -> None:
        """
        移除通知
        Returns: None

        """
        with self.uow.auto_complete():
            self.notify_repo.delete(notify)

    def send_mail_notify(self, potential_buyer: User, auction: Wish, auction_id) -> None:
        """
        透過email送出通知
        Args:
            potential_buyer: 有這項拍賣品需求的買家
            auction: 拍賣品資訊
            auction_id: 拍賣品id

        Returns: None

        """
        self.mailer.send_mail(
            to=potential_buyer.email,
            subject='[Roshpit WishList] Matches found',
            body=f'{auction.item.name}\r\n'
                 f'{os.linesep.join([wish_property.property.name + " " + str(wish_property.roll) + "" for wish_property in auction.wish_properties])}\r\n'
                 f'{"Level"} {str(auction.min_level)}\r\n'
                 f'{"Bid Price"} {str(auction.max_bid)}\r\n'
                 f'{"Buyout Price"} {str(auction.max_buyout)}\r\n'
                 f'https://www.roshpit.ca/market/auction/{auction_id}\r\n')

    def send_line_notify(self, potential_buyer: User, auction: Wish, auction_id) -> None:
        """
        透過line送出通知
        Args:
            potential_buyer: 有這項拍賣品需求的買家
            auction: 拍賣品資訊
            auction_id: 拍賣品id

        Returns: None

        """
        for notify in potential_buyer.notify:
            token = notify.id

            url = 'https://notify-api.line.me/api/notify'
            headers = {'Authorization': f'Bearer {token}'}

            data = urllib.parse.urlencode(
                {'message': f'\r\n'
                            f'{auction.item.name}\r\n'
                            f'{os.linesep.join([wish_property.property.name + " " + str(wish_property.roll) + "" for wish_property in auction.wish_properties])}\r\n'
                            f'{"Level"} {str(auction.min_level)}\r\n'
                            f'{"Bid Price"} {str(auction.max_bid)}\r\n'
                            f'{"Buyout Price"} {str(auction.max_buyout)}\r\n'
                            f'https://www.roshpit.ca/market/auction/{auction_id}\r\n'}

            ).encode('ascii')

            req = urllib.request.Request(url, data, headers)
            try:
                with urllib.request.urlopen(req) as response:
                    result = json.loads(response.read().decode('utf-8'))

            except urllib.error.HTTPError as e:
                if e.code == 401:
                    self.delete_notify(Notify(id=token))

    def notify_potential_buyer(self, auction: Wish, auction_id: str) -> None:
        """
        通知有這項拍賣品需求的買家
        Args:
            auction: 拍賣品資訊
            auction_id: 拍賣品id

        Returns: None

        """
        potential_buyers = self.find_potential_buyer(auction)

        if potential_buyers:
            for potential_buyer in potential_buyers:
                if potential_buyer.is_notification:
                    if potential_buyer.notification_method == '1':
                        self.send_mail_notify(potential_buyer, auction, auction_id)
                    else:
                        self.send_line_notify(potential_buyer, auction, auction_id)
