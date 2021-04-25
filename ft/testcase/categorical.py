from ft.testcase.variable import Variable

import numpy as np


class Categorical(Variable):
    value = None

    def __init__(self, all_values):
        self.all_values = all_values

    def random(self):
        self.value = (np.random.choice(self.all_values, 1))[0]

    def local_search(self):
        if len(self.all_values) == 1:
            return

        self.value = np.int64(self.value)
        cat_index = (np.where(self.all_values == self.value))[0][0]
        if cat_index == 0:  # current index = min index
            self.value = self.all_values[1]
        elif cat_index == len(self.all_values) - 1:  # current index = max index
            self.value = self.all_values[cat_index - 1]
        else:  # min index < current index < max index
            ran = np.random.random()
            if ran < 0.5:
                self.value = self.all_values[cat_index - 1]
            else:
                self.value = self.all_values[cat_index + 1]

    def random_in_range(self, value_1, value_2):
        if value_1 != value_2:
            value_1 = np.int64(value_1)
            value_2 = np.int64(value_2)

            cat_index_value_1 = np.where(self.all_values == value_1)
            cat_index_value_2 = np.where(self.all_values == value_2)

            cat_indices = np.array([cat_index_value_1[0][0], cat_index_value_2[0][0]])
            min_cat_index = np.min(cat_indices)
            max_cat_index = np.max(cat_indices)
            self.value = (np.random.choice(self.all_values[min_cat_index: max_cat_index + 1], 1))[0]
        else:
            self.random()
