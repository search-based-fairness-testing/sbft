from ft.ga.operators.mutation.mutation_function import MutationFunction
from ft.ga.operators.mutation.uniform_mutation import UniformMutation


class MutationFunctionFactory:

    @staticmethod
    def get_mutation_function(mutation_type, p_mutation, dimension):
        if mutation_type == "uniform":
            return UniformMutation(p_mutation, dimension)
        else:
            print('Error')
