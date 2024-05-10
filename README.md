# Chess Engine Experiments

Experiments with chess engines following the [book by Dominik Klein](https://arxiv.org/abs/2209.01506).

## Creating the Conda Environment

The commands are set-up to use mamba instead of conda. If you can't or don't want to use mamba, you can replace `mamba` by `conda` in the commands and scripts.

Create the environment:

    mamba env create -f environment.yml

Updating the environment after a change to the `environment.yml` file (this also creates a freeze of the new environment):

    ./update-environment.sh
