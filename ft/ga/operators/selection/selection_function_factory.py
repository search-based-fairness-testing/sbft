from ft.ga.operators.selection.fitness_proportionate_selection import FitnessProportionateSelection
from ft.utils.logging_utils import LoggingUtils


class SelectionFunctionFactory:

    @staticmethod
    def get_selection_function(selection_function_name):
        if selection_function_name == "roulette_wheel":
            return FitnessProportionateSelection()
        else:
            LoggingUtils.get_instance().error('[%s] Selection function type %s is not supported!' %
                                              (__class__.__name__, selection_function_name))
