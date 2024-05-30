# Chess Engine Experiments

Experiments with chess engines

## Creating the Conda Environment

The commands are set up to use mamba instead of conda. If you can't or don't want to use mamba, you can replace `mamba` by `conda` in the commands.

Create the environment:

```commandline
mamba env create -f environment.yml
```

Updating the environment after a change to the `environment.yml` file:

```commandline
mamba env update -f environment.yml
```
