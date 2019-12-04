from ..models.user import User
from ..repositories.base_user_repo import BaseUserRepo
from ..repositories.generic_repo import GenericRepo


class UserRepo(GenericRepo[User], BaseUserRepo):
    pass
