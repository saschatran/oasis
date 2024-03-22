#!/bin/bash

#SBATCH --ntasks=8
#SBATCH --mem-per-cpu=1024
#SBATCH --time=1:00:00
#SBATCH --job-name=oasis-estimation

path=$(pwd)
python main_estimation.py Feil $path/../Matsim_parameters_archive/students_dataset_fixed_biogeme_2609.joblib --fixed_vars gamma 1 Umin 0 --model_name Feil_oasis
