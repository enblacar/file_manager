!/bin/bash

#SBATCH --partition p_hpca4se
#SBATCH --nodelist catwoman
#SBATCH --mem 128000
#SBATCH --cpus-per-task 64
#SBATCH --job-name eblanco

source ~/.bashrc
hostname
date

./try.py
