from ft.testcase.variable_factory import VariableFactory
from ft.testcase.variable import Variable
import numpy as np


class TestCase:
    fitness = 0.0

    def __init__(self, dimension, variable_types, variable_bounds):
        self.test_input = np.empty(dimension, dtype=Variable)

        variable_index = 0
        for variable_type in variable_types:
            self.test_input[variable_index] = VariableFactory.get_variable(variable_type, variable_bounds[variable_index])
            variable_index += 1

    def get_test_input(self):
        return self.test_input

    def set_fitness(self, fitness):
        self.fitness = fitness

    def get_fitness(self):
        return self.fitness
