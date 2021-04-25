from ft.ga.operators.selection.selection import Selection

import numpy as np


class FitnessProportionateSelection(Selection):
    sum_fitness = 0.0

    def __init__(self):
        pass

    def calculate_sum_fitness(self, population):
        for testcase in population:
            self.sum_fitness += testcase.get_fitness()

    def select_parents(self, population, num_parents):
        if self.sum_fitness is None:
            self.calculate_sum_fitness(population)

        if self.sum_fitness == 0.0:
            return np.random.choice(population, num_parents)

        parents = list()
        for parent_index in range(0, num_parents):
            fitness_pos = np.random.random() * self.sum_fitness

            for testcase in population:
                fitness = testcase.get_fitness()

                if fitness >= fitness_pos:
                    parents.append(testcase)
                    break
                else:
                    fitness_pos = fitness_pos - fitness

        if len(parents) < num_parents:
            print('Execution should not reach here!')
            for parent_index in range(len(parents), num_parents):
                parents.append((np.random.choice(population, 1))[0])

        return parents
