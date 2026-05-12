#!/bin/bash
#SBATCH --job-name=mpi_lab3_tests
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --time=01:00:00
#SBATCH --output=tests_output.out
#SBATCH --error=tests_error.err

# Загрузить модули
module load intel/mpi4
module load intel/icc18

# Перейти в директорию работы
cd $SLURM_SUBMIT_DIR

# Проверка
echo "Working directory: $SLURM_SUBMIT_DIR"
echo "Number of tasks: $SLURM_NTASKS"

# 1. Создать данные
echo "Generating test matrices..."
python3 scripts/gen_matrix.py 500 data/input_A.txt
python3 scripts/gen_matrix.py 500 data/input_B.txt

# 2. Запустить тесты
echo "Running verification tests..."
srun -n 1 ./matrix_mult_mpi data/input_A.txt data/input_B.txt data/output_C.txt
srun -n 2 ./matrix_mult_mpi data/input_A.txt data/input_B.txt data/output_C.txt
srun -n 4 ./matrix_mult_mpi data/input_A.txt data/input_B.txt data/output_C.txt
srun -n 8 ./matrix_mult_mpi data/input_A.txt data/input_B.txt data/output_C.txt

# 3. Верификация
echo "Running verification..."
python3 scripts/verify.py data/input_A.txt data/input_B.txt data/output_C.txt

echo "Tests completed!"