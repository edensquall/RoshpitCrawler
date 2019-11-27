from ..models.notify import Notify
from ..repositories.base_notify_repo import BaseNotifyRepo
from ..repositories.generic_repo import GenericRepo


class NotifyRepo(GenericRepo[Notify], BaseNotifyRepo):
    pass
