#!/bin/bash

#SBATCH --ntasks=8
#SBATCH --mem-per-cpu=1024
#SBATCH --time=1:00:00
#SBATCH --job-name=oasis-estimation

path=$(pwd)
sbatch --ntasks=8 --mem-per-cpu=1024 --time=1:00:00 --job-name=run_matsim --wrap="python main_estimation.py MATSIM $path/../Matsim_parameters_archive/students_dataset_fixed_biogeme_2609.joblib"
