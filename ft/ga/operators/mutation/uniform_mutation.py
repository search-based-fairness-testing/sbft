from ft.ga.operators.mutation.mutation_function import MutationFunction
from ft.testcase.testcase import TestCase

import numpy as np
import copy


class UniformMutation(MutationFunction):

    def __init__(self, p_mutation, dimension):
        super().__init__(p_mutation, dimension)

    def mutate(self, solution):
        solution_copy = copy.deepcopy(solution)
        test_input_copy = solution_copy.get_test_input()
        for variable_index in range(0, self.dimension):
            ran_mutation = np.random.random()
            if ran_mutation < self.p_mutation:
                (test_input_copy[variable_index]).random()

        return solution_copy
