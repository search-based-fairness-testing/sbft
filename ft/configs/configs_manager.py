import os
import yaml


class ConfigsManager:
    configs_file = 'configs.yml'
    instance = None

    time_budget = 3600
    proportion_test_insertion = 0.1
    p_crossover = 0.75
    p_mutation = 0.7
    population_size = 100
    p_cache = 0.5
    max_generations = 100
    crossover_type = 'uniform'
    mutation_type = 'uniform'
    parent_selection_type = 'roulette_wheel'

    protected_features = list()
    model_filepath = ''
    variable_boundaries_filepath = ''
    valid_inputs_dir = ''
    categorical_variables_dir = ''

    def __init__(self, workspace_dir):
        self.workspace_dir = workspace_dir

    def get_yaml_configs(self):
        yaml_path = os.path.join(self.workspace_dir, self.configs_file)
        configs = {}
        if os.path.exists(yaml_path):
            stream = open(yaml_path, "r")
            configs = yaml.load(stream)

        return configs

    @staticmethod
    def get_instance(workspace_dir):
        if ConfigsManager.instance is None:
            ConfigsManager.instance = ConfigsManager(workspace_dir)

        return ConfigsManager.instance

    def load_configs(self):
        configs = self.get_yaml_configs()
        self.time_budget = configs.get('ga_parameters').get('time_budget')
        self.proportion_test_insertion = configs.get('ga_parameters').get('proportion_test_insertion')
        self.p_crossover = configs.get('ga_parameters').get('p_crossover')
        self.p_mutation = configs.get('ga_parameters').get('p_mutation')
        self.population_size = configs.get('ga_parameters').get('population_size')
        self.p_cache = configs.get('ga_parameters').get('p_cache')
        self.max_generations = configs.get('ga_parameters').get('max_generations')
        self.crossover_type = configs.get('ga_parameters').get('crossover_type')
        self.mutation_type = configs.get('ga_parameters').get('mutation_type')
        self.parent_selection_type = configs.get('ga_parameters').get('parent_selection_type')

        self.protected_features = [configs.get('sut_settings').get('protected_features')]
        self.model_filepath = configs.get('sut_settings').get('model_filepath')
        self.variable_boundaries_filepath = configs.get('sut_settings').get('variable_boundaries_filepath')
        self.valid_inputs_dir = configs.get('sut_settings').get('valid_inputs_dir')
        self.categorical_variables_dir = configs.get('sut_settings').get('categorical_variables_dir')
