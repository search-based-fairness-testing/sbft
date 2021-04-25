import copy
import numpy as np


class MutationFunction:

    def __init__(self, p_mutation, dimension):
        self.p_mutation = p_mutation
        self.dimension = dimension

    def mutate(self, solution):
        pass

    def mutate_middle(self, solution, parent_1, parent_2):
        solution_copy = copy.deepcopy(solution)
        test_input_copy = solution_copy.get_test_input()

        test_input_parent_1 = parent_1.get_test_input()
        test_input_parent_2 = parent_2.get_test_input()
        for variable_index in range(0, self.dimension):
            ran_mutation = np.random.random()
            if ran_mutation < self.p_mutation:
                (test_input_copy[variable_index]).random_in_range((test_input_parent_1[variable_index]).get_value(),
                                                                  (test_input_parent_2[variable_index]).get_value())

        return solution_copy
