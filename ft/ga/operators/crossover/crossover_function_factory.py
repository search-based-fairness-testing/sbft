from ft.ga.operators.crossover.crossover_function import CrossoverFunction
from ft.ga.operators.crossover.uniform_crossover import UniformCrossover


class CrossoverFunctionFactory:

    @staticmethod
    def get_crossover_function(crossover_type, p_crossover, dimension):
        if crossover_type == "uniform":
            return UniformCrossover(p_crossover, dimension)
        else:
            print('Error')
