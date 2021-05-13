import numpy as np
import datetime
import collections
import copy
import math

from ft.testcase.testcase import TestCase
from ft.loggers.logger_factory import LoggerFactory


class GeneticAlgorithm:

    def __init__(self, ga_operators, ga_parameters, sut_settings):
        self.logger = LoggerFactory.get_logger(__class__.__name__)

        self.fitness_function = ga_operators['fitness_function']
        self.crossover_function = ga_operators['crossover']
        self.mutation_function = ga_operators['mutation']
        self.selection_function = ga_operators['selection']

        self.max_generations = ga_parameters['max_generations']
        self.population_size = ga_parameters['population_size']
        self.max_time = ga_parameters['max_time']
        self.proportion_test_insertion = ga_parameters['proportion_test_insertion']

        self.variable_types = sut_settings['variable_types']
        self.variable_bounds = sut_settings['variable_bounds']
        self.dimension = sut_settings['dimension']

        self.input_validate_function = sut_settings['input_validate_function']

        self.start_time = None
        self.current_generation = 0
        self.population = np.empty(self.population_size, dtype=TestCase)
        self.fitnesses = dict()     # population_index -> fitness

        self.num_test_insertion = math.ceil(self.proportion_test_insertion * self.population_size)

        self.archive_test_inputs = False

    def generate_random_solution(self, testcase):
        for variable in testcase.get_test_input():
            variable.random()

        self.input_validate_function(testcase.get_test_input())

    def archive_test_input(self, testcase):
        pass

    def initialise_population(self):
        self.logger.debug('Initialising population...')

        for population_index in range(0, self.population_size):
            self.population[population_index] = TestCase(self.dimension, self.variable_types, self.variable_bounds)
            testcase = self.population[population_index]
            self.generate_random_solution(testcase)
            self.fitnesses[population_index] = self.fitness_function.evaluate_fitness(testcase)

            self.logger.debug('Population index - %d | [%s]' % (population_index, testcase.to_string()))

            if self.archive_test_inputs:
                self.archive_test_input(testcase)

        self.logger.debug('Finished initialising population.')

    def time_taken_since_start(self):
        current_time = datetime.datetime.now()
        run_time = current_time - self.start_time
        run_time_sec = int(run_time.total_seconds())
        return run_time_sec

    def stopping_criteria(self):
        self.logger.debug('Current generation - %d, max generations - %d' % (self.current_generation, self.max_generations))
        if self.current_generation > self.max_generations:
            return True

        run_time_sec = self.time_taken_since_start()
        self.logger.debug('Current run time - %d seconds, maximum run time - %d seconds' % (run_time_sec, self.max_time))
        if run_time_sec > self.max_time:
            return True
        else:
            return False

    def local_search(self, solution):
        self.logger.debug('Local search on the best solution in the current population.')
        self.logger.debug('Best solution - %s' % solution.to_string())

        search_order = list()
        for index in range(0, len(self.variable_types)):
            search_order.append(index)
        np.random.shuffle(search_order)
        self.logger.debug('Order of variables to perform the local search (indices) %s' % str(search_order))

        current_fitness = solution.get_fitness()
        self.logger.debug('Current fitness - %.4f' % current_fitness)

        for index in search_order:
            solution_copy = copy.deepcopy(solution)
            test_input_copy = solution_copy.get_test_input()

            (test_input_copy[index]).local_search()
            self.input_validate_function(test_input_copy)
            new_fitness = self.fitness_function.evaluate_fitness(solution_copy)
            self.logger.debug('Intermediary solution - %s' % solution_copy.to_string())
            self.logger.debug('New fitness - %.4f | Current fitness - %.4f' % (new_fitness, current_fitness))

            if self.archive_test_inputs:
                self.archive_test_input(solution_copy)

            if new_fitness > current_fitness:
                current_fitness = new_fitness
                solution = solution_copy

        self.logger.debug('Local search finished. Returning the best solution - %s' % solution.to_string())

        return solution

    def breed_next_generation(self):
        self.logger.debug('Start breeding next generation...')
        offspring_population = np.empty(self.population_size + self.num_test_insertion, dtype=TestCase)

        for offspring_round_index in range(0, int(self.population_size / 2)):
            self.logger.debug('Offspring round index - %d | selecting parents...' % offspring_round_index)
            parents = self.selection_function.select_parents(self.population, 2)
            self.logger.debug('Offspring round index - %d | parent 1 (ignore fitness) - [%s]' % (offspring_round_index, parents[0].to_string()))
            self.logger.debug('Offspring round index - %d | parent 2 (ignore fitness) - [%s]' % (offspring_round_index, parents[1].to_string()))

            self.logger.debug('Offspring round index - %d | crossing over parents...' % offspring_round_index)
            children_interim = self.crossover_function.crossover(parents[0], parents[1])
            self.logger.debug('Offspring round index - %d | child interim 1 (ignore fitness) - [%s]' % (offspring_round_index, children_interim[0].to_string()))
            self.logger.debug('Offspring round index - %d | child interim 2 (ignore fitness) - [%s]' % (offspring_round_index, children_interim[1].to_string()))
            self.input_validate_function(children_interim[0].get_test_input())
            self.input_validate_function(children_interim[1].get_test_input())

            self.logger.debug('Offspring round index - %d | Mutating interim child 1...' % offspring_round_index)
            child_1 = self.mutation_function.mutate(children_interim[0])
            self.logger.debug('Offspring round index - %d | child 1 (ignore fitness) - [%s]' % (offspring_round_index, child_1.to_string()))
            self.input_validate_function(child_1.get_test_input())

            self.logger.debug('Offspring round index - %d | Mutating interim child 2 in middle of parents...' % offspring_round_index)
            child_2 = self.mutation_function.mutate_middle(children_interim[1], parents[0], parents[1])
            self.logger.debug('Offspring round index - %d | child 2 (ignore fitness) - [%s]' % (offspring_round_index, child_2.to_string()))
            self.input_validate_function(child_2.get_test_input())

            self.fitnesses[self.population_size + offspring_round_index * 2] = self.fitness_function.evaluate_fitness(child_1)
            self.fitnesses[self.population_size + offspring_round_index * 2 + 1] = self.fitness_function.evaluate_fitness(child_2)

            offspring_population[offspring_round_index * 2] = child_1
            offspring_population[offspring_round_index * 2 + 1] = child_2
            self.logger.debug('Offspring population index - %d | child 1 - [%s]' % (offspring_round_index * 2, child_1.to_string()))
            self.logger.debug('Offspring population index - %d | child 2 - [%s]' % (offspring_round_index * 2 + 1, child_2.to_string()))

            if self.archive_test_inputs:
                self.archive_test_input(child_1)
                self.archive_test_input(child_2)

        for test_insertion_index in range(0, self.num_test_insertion):
            testcase = TestCase(self.dimension, self.variable_types, self.variable_bounds)
            self.generate_random_solution(testcase)
            self.fitnesses[self.population_size * 2 + test_insertion_index] = self.fitness_function.evaluate_fitness(testcase)

            offspring_population[self.population_size + test_insertion_index] = testcase
            self.logger.debug('Test insertion index - %d | [%s]' % (test_insertion_index, testcase.to_string()))

            if self.archive_test_inputs:
                self.archive_test_input(testcase)

        self.logger.debug('Finished breeding next generation.')
        return offspring_population

    def elitism(self, union_population):
        fitnesses_sorted = list(collections.OrderedDict(
            sorted(self.fitnesses.items(), key=lambda item: item[1], reverse=True)).keys())
        for index in range(0, self.population_size):
            self.population[index] = union_population[fitnesses_sorted[index]]

    def evolve(self):
        offspring_population = self.breed_next_generation()
        union_population = np.concatenate([self.population, offspring_population])
        self.elitism(union_population)

        best_solution = self.local_search(self.population[0])
        self.population[0] = best_solution

        self.current_generation += 1

    def run(self):
        self.logger.debug('Start running genetic algorithm...')
        self.start_time = datetime.datetime.now()
        self.initialise_population()

        fitnesses_sorted = list(collections.OrderedDict(
            sorted(self.fitnesses.items(), key=lambda item: item[1], reverse=True)).keys())
        self.logger.debug('Population indices sorted by fitness - %s' % str(fitnesses_sorted))

        # sort the population
        self.logger.debug('Sorting the population...')
        population_copy = np.empty_like(self.population)
        population_copy[:] = self.population
        for index in range(0, self.population_size):
            self.population[index] = population_copy[fitnesses_sorted[index]]
            self.fitnesses[index] = self.population[index].get_fitness()
            self.logger.debug('Population index - %d | [%s]' % (index, self.population[index].to_string()))

        best_solution = self.local_search(self.population[0])
        self.population[0] = best_solution
        self.fitnesses[0] = best_solution.get_fitness()

        self.current_generation = 0
        self.logger.debug('current generation - %d, current fitness - %.4f' % (self.current_generation,
                                                                               self.fitnesses[0]))

        self.logger.debug('Start evolving test cases...')
        while not self.stopping_criteria():
            self.evolve()

        return self.population[0].get_fitness()
