#!/bin/bash


path=$(pwd)

sbatch --ntasks=16 --mem-per-cpu=1024 --time=2:00:00 --job-name=run_feil --wrap="python main_estimation.py Feil $path/../Matsim_parameters_archive/students_dataset_fixed_biogeme_2609.joblib"
