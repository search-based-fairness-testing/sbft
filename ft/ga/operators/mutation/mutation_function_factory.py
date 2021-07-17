from ft.ga.operators.mutation.mutation_function import MutationFunction
from ft.ga.operators.mutation.uniform_mutation import UniformMutation
from ft.utils.logging_utils import LoggingUtils


class MutationFunctionFactory:

    @staticmethod
    def get_mutation_function(mutation_type, p_mutation, dimension):
        if mutation_type == "uniform":
            return UniformMutation(p_mutation, dimension)
        else:
            LoggingUtils.get_instance().error('[%s] Mutation type %s is not supported!' %
                                              (__class__.__name__, mutation_type))
