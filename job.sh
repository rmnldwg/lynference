#!/usr/bin/env bash
#SBATCH --cpus-per-task=1
#SBATCH --mem=2000
#SBATCH --time=2-00:00:00
#SBATCH --output=job.log

module load anaconda3
source activate graph-ext

srun python -m dvc update -R data
srun python -m dvc repro
