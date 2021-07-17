from ft.ga.operators.crossover.crossover_function import CrossoverFunction
from ft.ga.operators.crossover.uniform_crossover import UniformCrossover
from ft.utils.logging_utils import LoggingUtils


class CrossoverFunctionFactory:

    @staticmethod
    def get_crossover_function(crossover_type, p_crossover, dimension):
        if crossover_type == "uniform":
            return UniformCrossover(p_crossover, dimension)
        else:
            LoggingUtils.get_instance().error('[%s] Crossover type %s is not supported!' %
                                              (__class__.__name__, crossover_type))
