#!/bin/bash
#SBATCH --job-name=qpt
#SBATCH --output=qpt_output.out
#SBATCH --error=qpt_error.err
#SBATCH --partition qpu     
#SBATCH --nodes 1           # Number of nodes
#SBATCH --ntasks 1          # Total number of MPI tasks 
#SBATCH --cpus-per-task 1   # Cores per task
#SBATCH --mem-per-cpu 4G    # Memory per core
#SBATCH --time 02:00:00     # Max run time (hh:mm:ss)

module purge

module load qmio/hpc gcc/12.3.0 qmio-tools/0.2.0-python-3.9.9 qiskit/1.2.4-python-3.9.9

# ---------------------------------------------------------------------------- #
#                    HOW TO USE LIBRARIES NOT INCLUDED ABOVE                   #
# ---------------------------------------------------------------------------- #
# If we want to use external libraries added to the loaded ones, we can create a
# virtual environment with system site access. 
# To do that, in a terminal run the commands:

# module purge
# module load qmio/hpc gcc/12.3.0 qmio-tools/0.2.0-python-3.9.9 qiskit/1.2.4-python-3.9.9
# python -m venv --system-site-packages PATH_NOMBRE_DEL_VENV 

# We activate the venv 
# source PATH_NOMBRE_DEL_VENV/bin/activate
# Now with the python activated we install here the packages we want with pip install ... 



# ---------------------------------------------------------------------------- #
#              IN CASE WE WANT TO USE THE VENV EXPLAINED, UNCOMMENT THIS       #
# ---------------------------------------------------------------------------- #
# source PATH_NOMBRE_DEL_VENV/bin/activate


python NOMBRE_DEL_PROGRAMA.py 

# IF ur program receives command line arguments, you must also write them here.
# Example : python NOMBRE_DEL_PROGRAMA.py  --config config.json


# To send this job, run: sbatch job.sh
