#/bin/sh

mamba env update -f environment.yml
mamba env export -n coding-challenge --file environment_freeze.yml
