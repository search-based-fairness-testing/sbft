from ft.testcase.testcase import TestCase
from ft.testcase.variable import Variable

import numpy as np
from sklearn.ensemble import RandomForestRegressor


class FitnessFunction:

    def __init__(self, model, protected_indices, protected_variables, p_cache):
        self.model = model
        self.protected_indices = protected_indices      # protected_feature -> protected_feature_index
        self.p_cache = p_cache
        self.protected_variables = protected_variables      # protected_feature -> protected_variable (Variable) of size 2

        self.best_values = dict()  # protected_feature -> value_1, value_2
        self.best_output_diff = 0.0

    def evaluate_fitness(self, solution):
        test_input_1 = np.array([variable.get_value() for variable in solution.get_test_input()])
        test_input_2 = np.array([variable.get_value() for variable in solution.get_test_input()])

        # test_input_1 = np.array(solution.get_test_input().copy())
        # test_input_2 = np.array(solution.get_test_input().copy())

        current_values = dict()  # protected_feature -> value_1, value_2
        ran = np.random.random()
        if ran < self.p_cache and len(self.best_values) > 0:
            for protected_feature in self.protected_indices.keys():
                values = self.best_values[protected_feature]
                protected_index = self.protected_indices[protected_feature]
                test_input_1 = np.insert(test_input_1, protected_index, values[0].copy())
                test_input_2 = np.insert(test_input_2, protected_index, values[1].copy())
                current_values = self.best_values
        else:
            # TODO: Check if both values are equal
            for protected_feature in self.protected_indices.keys():
                (self.protected_variables[protected_feature])[0].random()
                value_1 = (self.protected_variables[protected_feature])[0].get_value()

                (self.protected_variables[protected_feature])[1].random()
                value_2 = (self.protected_variables[protected_feature])[1].get_value()

                values = [value_1, value_2]

                protected_index = self.protected_indices[protected_feature]
                test_input_1 = np.insert(test_input_1, protected_index, values[0].copy())
                test_input_2 = np.insert(test_input_2, protected_index, values[1].copy())

                current_values[protected_feature] = values

        input_1 = np.array(test_input_1, ndmin=2)
        input_2 = np.array(test_input_2, ndmin=2)

        output_1 = self.model.predict(input_1)
        output_2 = self.model.predict(input_2)

        output_diff = np.abs(output_1 - output_2)
        if output_diff > self.best_output_diff:
            self.best_values = current_values
            self.best_output_diff = output_diff

        fitness = output_diff
        solution.set_fitness(fitness)
        return fitness
