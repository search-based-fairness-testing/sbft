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
        self.population = np.array([TestCase(self.dimension, self.variable_types, self.variable_bounds)] * self.population_size)

        for population_index in range(0, self.population_size):
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
        if self.current_generation > self.max_generations:
            return True

        run_time_sec = self.time_taken_since_start()
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
        offspring_population = np.empty(self.population_size + self.num_test_insertion, dtype=TestCase)

        for offspring_round_index in range(0, int(self.population_size / 2)):
            parents = self.selection_function.select_parents(self.population, 2)

            children_interim = self.crossover_function.crossover(parents[0], parents[1])
            self.input_validate_function(children_interim[0].get_test_input())
            self.input_validate_function(children_interim[1].get_test_input())

            child_1 = self.mutation_function.mutate(children_interim[0])
            self.input_validate_function(child_1.get_test_input())

            child_2 = self.mutation_function.mutate_middle(children_interim[1], parents[0], parents[1])
            self.input_validate_function(child_2.get_test_input())

            self.fitnesses[self.population_size + offspring_round_index * 2] = self.fitness_function.evaluate_fitness(child_1)
            self.fitnesses[self.population_size + offspring_round_index * 2 + 1] = self.fitness_function.evaluate_fitness(child_2)

            offspring_population[offspring_round_index * 2] = child_1
            offspring_population[offspring_round_index * 2 + 1] = child_2

            if self.archive_test_inputs:
                self.archive_test_input(child_1)
                self.archive_test_input(child_2)

        for test_insertion_index in range(0, self.num_test_insertion):
            testcase = TestCase(self.dimension, self.variable_types, self.variable_bounds)
            self.generate_random_solution(testcase)
            self.fitnesses[self.population_size * 2 + test_insertion_index] = self.fitness_function.evaluate_fitness(testcase)

            offspring_population[self.population_size + test_insertion_index] = testcase

            if self.archive_test_inputs:
                self.archive_test_input(testcase)

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

        pop_index_best_fitness = fitnesses_sorted[0]    # next(iter(fitnesses_sorted.keys()))
        best_solution = self.local_search(self.population[pop_index_best_fitness])
        self.population[pop_index_best_fitness] = best_solution
        fitnesses_sorted[0] = best_solution.get_fitness()

        self.current_generation = 0
        self.logger.debug('current generation - %d, current fitness - %.4f' % (self.current_generation,
                                                                               fitnesses_sorted[0]))

        # sort the population
        population_copy = self.population
        for index in range(0, self.population_size):
            self.population[index] = population_copy[fitnesses_sorted[index]]

        while not self.stopping_criteria():
            self.evolve()

        return self.population[0].get_fitness()
