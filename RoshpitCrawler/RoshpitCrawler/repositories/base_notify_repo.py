from abc import abstractmethod
from typing import List

from ..models.notify import Notify
from ..repositories.base_repo import BaseRepo


class BaseNotifyRepo(BaseRepo[Notify]):

    pass
