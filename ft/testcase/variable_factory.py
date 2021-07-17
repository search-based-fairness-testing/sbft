from ft.testcase.integer import Integer
from ft.testcase.real import Real
from ft.testcase.categorical import Categorical
from ft.utils.logging_utils import LoggingUtils


class VariableFactory:

    @staticmethod
    def get_variable(variable_type, variable_bound):
        if variable_type == "int":
            return Integer(variable_bound[0], variable_bound[1])
        elif variable_type == "real":
            return Real(variable_bound[0], variable_bound[1])
        elif variable_type == "cat":
            return Categorical(variable_bound)
        else:
            LoggingUtils.get_instance().error('[%s] Variable type %s is not supported!' %
                                              (__class__.__name__, variable_type))
