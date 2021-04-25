from ft.testcase.variable import Variable

import numpy as np


class Integer(Variable):
    value = 0

    def __init__(self, lower_bound, upper_bound):
        self.lower_bound = int(lower_bound)
        self.upper_bound = int(upper_bound)

    def random(self):
        self.value = np.random.randint(self.lower_bound, self.upper_bound + 1)

    def local_search(self):
        if self.lower_bound == self.upper_bound:
            return
        elif self.value == self.lower_bound:  # current value = min value
            self.value = self.value + 1
        elif self.value == self.upper_bound:  # current value = max value
            self.value = self.value - 1
        else:  # min < current value < max
            ran = np.random.random()
            if ran < 0.5:
                self.value = self.value - 1
            else:
                self.value = self.value + 1

    def random_in_range(self, value_1, value_2):
        value_min = min(value_1, value_2)
        value_max = max(value_1, value_2)

        if value_min != value_max:
            self.value = np.random.randint(value_min, value_max)
        else:
            self.random()
