from ..models.parameter import Parameter
from ..repositories.base_parameter_repo import BaseParameterRepo
from ..repositories.generic_repo import GenericRepo


class ParameterRepo(GenericRepo[Parameter], BaseParameterRepo):
    pass
