#!/bin/bash

#SBATCH --ntasks=8
#SBATCH --mem-per-cpu=1024
#SBATCH --time=1:00:00
#SBATCH --job-name=oasis-estimation

module load gcc/8.2.0 python_gpu/3.10.4
python main_estimation.py Linear_OASIS /cluster/home/mfrancesc/IVT/oasis/examples_files/MATSIM_parameters_archive/students_dataset_fixed_biogeme_2609.joblib