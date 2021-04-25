import copy
import numpy as np

from ft.ga.operators.crossover.crossover_function import CrossoverFunction


class UniformCrossover(CrossoverFunction):

    def __init__(self, p_crossover, dimension):
        super().__init__(p_crossover, dimension)

    def crossover(self, parent_1, parent_2):
        child_1 = copy.deepcopy(parent_1)
        child_2 = copy.deepcopy(parent_2)

        ran_crossover = np.random.random()
        if ran_crossover >= self.p_crossover:
            return np.array([child_1, child_2])
        else:
            test_input_child_1 = child_1.get_test_input()
            test_input_child_2 = child_2.get_test_input()
            test_input_parent_1 = parent_1.get_test_input()
            test_input_parent_2 = parent_2.get_test_input()

            for variable_index in range(0, self.dimension):
                ran_uniform = np.random.random()
                if ran_uniform < 0.5:
                    (test_input_child_1[variable_index]).set_value((test_input_parent_2[variable_index]).get_value())
                    (test_input_child_2[variable_index]).set_value((test_input_parent_1[variable_index]).get_value())

            return np.array([child_1, child_2])
