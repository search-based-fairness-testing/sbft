from ft.testcase.variable import Variable
import numpy as np


class Real(Variable):
    value = 0.0

    def __init__(self, lower_bound, upper_bound):
        self.lower_bound = float(lower_bound)
        self.upper_bound = float(upper_bound)

    def random(self):
        self.value = self.lower_bound + np.random.random() * (self.upper_bound - self.lower_bound)

    def local_search(self):
        if self.lower_bound == self.upper_bound:
            return
        elif self.value == self.lower_bound:  # current value = min value
            self.value = self.value + 1.0
        elif self.value == self.upper_bound:  # current value = max value
            self.value = self.value - 1.0
        else:  # min < current value < max
            ran = np.random.random()
            if ran < 0.5:
                self.value = self.value - 1.0
            else:
                self.value = self.value + 1.0

        if self.value < self.lower_bound:  # new value < min value
            self.value = self.lower_bound
        elif self.value > self.upper_bound:  # new value > max value
            self.value = self.upper_bound

    def random_in_range(self, value_1, value_2):
        value_min = min(value_1, value_2)
        value_max = max(value_1, value_2)

        if value_min != value_max:
            self.value = value_min + np.random.random() * (value_max - value_min)
        else:
            self.random()
