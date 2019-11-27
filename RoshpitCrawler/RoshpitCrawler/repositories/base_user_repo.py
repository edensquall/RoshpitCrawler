from abc import abstractmethod

from ..models.user import User
from ..repositories.base_repo import BaseRepo


class BaseUserRepo(BaseRepo[User]):

    pass