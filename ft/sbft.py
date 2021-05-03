import numpy as np
import datetime
import os
import pickle
import math
import pandas as pd
import sys

from ft.ga.fitness_function import FitnessFunction
from ft.testcase.variable_factory import VariableFactory
from ft.ga.operators.crossover.crossover_function_factory import CrossoverFunctionFactory
from ft.ga.operators.mutation.mutation_function_factory import MutationFunctionFactory
from ft.ga.operators.selection.selection_function_factory import SelectionFunctionFactory
from ft.ga.genetic_algorithm import GeneticAlgorithm
from ft.configs.configs_manager import ConfigsManager
from ft.loggers.logger_factory import LoggerFactory


WORKSPACE_DIR = sys.argv[1]


def main():
    sbft = SBFT()
    sbft.run()


class SBFT:

    def __init__(self):
        self.configs_manager = ConfigsManager.create_instance(WORKSPACE_DIR)
        self.logger = LoggerFactory.get_logger(__class__.__name__)

    def load_object(self, filename):
        with open(filename, 'rb') as file:
            object_o = pickle.load(file)
        return object_o

    def load_valid_inputs(self, valid_inputs_dir, valid_inputs, feature):
        valid_inputs_fp = os.path.join(valid_inputs_dir, feature + '.csv')
        if os.path.exists(valid_inputs_fp):
            valid_inputs_df = pd.read_csv(valid_inputs_fp)
            valid_inputs[feature] = np.array(valid_inputs_df['code'])

    def is_cat_var(self, cat_vars_dir, feature):
        cat_vars_fp = os.path.join(cat_vars_dir, feature + '.csv')
        if os.path.exists(cat_vars_fp):
            return True

        return False

    def load_categories(self, cat_vars_dir, feature):
        cat_vars_fp = os.path.join(cat_vars_dir, feature + '.csv')
        cat_vars_df = pd.read_csv(cat_vars_fp)
        return cat_vars_df['code'].tolist()

    def run(self):
        # configs_manager = ConfigsManager.create_instance(WORKSPACE_DIR)
        self.configs_manager.load_configs()

        self.logger.debug('Loaded Configurations.')

        time_budget = self.configs_manager.time_budget
        proportion_test_insertion = self.configs_manager.proportion_test_insertion
        p_crossover = self.configs_manager.p_crossover
        p_mutation = self.configs_manager.p_mutation
        population_size = self.configs_manager.population_size
        p_cache = self.configs_manager.p_cache
        max_generations = self.configs_manager.max_generations

        crossover_type = self.configs_manager.crossover_type
        mutation_type = self.configs_manager.mutation_type
        parent_selection_type = self.configs_manager.parent_selection_type

        protected_features = self.configs_manager.protected_features

        model_filepath = self.configs_manager.model_filepath

        model_pyobject = self.load_object(model_filepath)
        features = model_pyobject['features']
        model = model_pyobject['model']

        # variables and their bounds
        var_bound_fp = self.configs_manager.variable_boundaries_filepath
        var_bound_df = pd.read_csv(var_bound_fp)

        var_types = []
        var_bounds = []
        var_types_protected = dict()
        var_bounds_protected = dict()

        valid_inputs = dict()

        for feature in features:
            self.load_valid_inputs(self.configs_manager.valid_inputs_dir, valid_inputs, feature)
            if self.is_cat_var(self.configs_manager.categorical_variables_dir, feature):
                all_categories = self.load_categories(self.configs_manager.categorical_variables_dir, feature)
                if feature in protected_features:
                    var_bounds_protected[feature] = all_categories
                    var_types_protected[feature] = 'cat'
                else:
                    var_bounds.append(all_categories)
                    var_types.append('cat')
            else:
                feature_index = 0
                for feature_in_df in var_bound_df['feature']:
                    if feature in feature_in_df:
                        break
                    feature_index += 1

                min = var_bound_df.at[feature_index, 'min']
                max = var_bound_df.at[feature_index, 'max']
                bounds = [min, max]

                if feature in protected_features:
                    var_bounds_protected[feature] = bounds
                else:
                    var_bounds.append(bounds)

                type_name = var_bound_df.at[feature_index, 'type']
                assert type_name != 'cat'

                if feature in protected_features:
                    var_types_protected[feature] = type_name
                else:
                    var_types.append(type_name)

        var_types = np.array(var_types)
        var_bounds = np.array(var_bounds, dtype=list)

        protected_indices = dict()
        protected_variables = dict()
        for protected_feature in protected_features:
            indices = [i for i, s in enumerate(features) if protected_feature in s]
            protected_indices[protected_feature] = indices[0]

            protected_variable_1 = VariableFactory.get_variable(var_types_protected[protected_feature],
                                                                var_bounds_protected[protected_feature])

            protected_variable_2 = VariableFactory.get_variable(var_types_protected[protected_feature],
                                                                var_bounds_protected[protected_feature])

            protected_variables[protected_feature] = [protected_variable_1, protected_variable_2]

        # genetic algorithm parameters
        ga_parameters = {'max_generations': max_generations, 'population_size': population_size, 'max_time': time_budget,
                         'proportion_test_insertion': proportion_test_insertion}

        # SUT settings
        sut_settings = {'variable_types': var_types, 'variable_bounds': var_bounds, 'dimension': len(var_types),
                        'input_validate_function': self.validate_input}

        fitness_function = FitnessFunction(model, protected_indices, protected_variables, p_cache)
        crossover_function = CrossoverFunctionFactory.get_crossover_function(crossover_type, p_crossover, len(var_types))
        mutation_function = MutationFunctionFactory.get_mutation_function(mutation_type, p_mutation, len(var_types))
        selection_function = SelectionFunctionFactory.get_selection_function(parent_selection_type)

        ga_operators = {'fitness_function': fitness_function, 'crossover': crossover_function,
                        'mutation': mutation_function, 'selection': selection_function}

        genetic_algorithm = GeneticAlgorithm(ga_operators, ga_parameters, sut_settings)
        fairness_degree = genetic_algorithm.run()
        print('Fairness Degree: %f' % fairness_degree)

    @staticmethod
    def validate_input(test_input):
        pass


if __name__ == '__main__':
    sbft = SBFT()
    sbft.run()
