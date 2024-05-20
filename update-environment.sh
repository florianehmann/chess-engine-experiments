#/bin/sh

mamba env update -f environment.yml
mamba env export -n chess --file environment_freeze.yml
