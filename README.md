# SBFT: Search-Based Fairness Testing
SBFT is a fairness testing tool for regression-based AI software. It estimates the _fairness degree (D)_ of the system under test. Fariness degree is defined as follows.

Given an AI software system, the **fairness degree** is measured by the
maximum difference in the predicted values by the AI software for all
pairs of instances (*x*<sub>*i*</sub>,*x*<sub>*j*</sub>) that are
identical apart from the sensitive attribute, i.e.,
*x*<sub>*i*</sub><sup>*s*</sup> ≠ *x*<sub>*j*</sub><sup>*s*</sup>.

*D* = max<sub>∀*i*, *j*</sub>\|*y*<sub>*i*</sub>−*y*<sub>*j*</sub>\|; *x*<sub>*i*</sub><sup>*s*</sup> ≠ *x*<sub>*j*</sub><sup>*s*</sup> & *x*<sub>*i*</sub><sup>*k*</sup> = *x*<sub>*j*</sub><sup>*k*</sup>; ∀*k* ≠ *s*

where *y*<sub>*i*</sub> and *y*<sub>*j*</sub> are the outputs for inputs *x*<sub>*i*</sub> and *x*<sub>*i*</sub>.

# How to use SBFT?

Parameter Settings
------------

All the parameters are defined in [configs.yml](https://github.com/search-based-fairness-testing/sbft/blob/5d3f9d81180bbd8ae263fc271bdd8c5de6f1a799/configs.yml)

| Parameter                 | Description                                      | Default Value  | 
|---------------------------|--------------------------------------------------|---------------:|
| time_budget               | Execution time (seconds)                         |     7200       | 
| proportion_test_insertion | Rate of random test insertion in every iteration |      0.1       |
| p_crossover               | Crossover probability                            |     0.75       |
| p_mutation                | Mutation probability                             |      0.8       | 
| population_size           | Population size                                  |      100       |
| p_cache                   | Probability of using cache in fitness evaluation |      0.5       |
| max_generations           | Maximum number of generations                    |     1000       |
| crossover_type            | Crossover type                                   |  uniform       |
| mutation_type             | Mutation type                                    |  uniform       |
| parent_selection_type     | Parent selection type                            | roulette_wheel |
| protected_features        | Sensitive attributes, i.e., protected features   |        -       |
| model_filepath            | Filepath to the model                            |        -       |
| variable_boundaries_filepath | Filepath to the variable boundaries file      |        -       |
| valid_inputs_dir             | Path to the directory containing valid inputs for categorical variables |        -       |
| categorical_variables_dir    | Path to the directory containing categorical variables                  |        -       |
| primary_logger_type          | Primary logger type                           |   console      |

Steps to Run SBFT
------------

Currently, SBFT can be run by executing the source code.

1. Clone SBFT:

    - `git clone https://github.com/search-based-fairness-testing/sbft.git`

2. Configure the parameters listed above and locate the [configs.yml](https://github.com/search-based-fairness-testing/sbft/blob/5d3f9d81180bbd8ae263fc271bdd8c5de6f1a799/configs.yml) file in the workspace directory.

3. Run SBFT

    - `cd sbft`
    - `python3 -u ft/sbft.py <path to workspace dir>`

# Publications
