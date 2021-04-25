from ft.ga.operators.selection.fitness_proportionate_selection import FitnessProportionateSelection


class SelectionFunctionFactory:

    @staticmethod
    def get_selection_function(selection_function_name):
        if selection_function_name == "roulette_wheel":
            return FitnessProportionateSelection()
        else:
            print('Error')
