#!/bin/bash

#SBATCH --ntasks=8
#SBATCH --mem-per-cpu=1024
#SBATCH --time=1:00:00
#SBATCH --job-name=oasis-estimation

curl -d "Start linear_oasis at" ntfy.sh/oasis
path=$(pwd)
python main_estimation.py Linear_OASIS $path/../Matsim_parameters_archive/students_dataset_fixed_biogeme_2609.joblib

curl -d "linear oasis done" ntfy.sh/oasis

