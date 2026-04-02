#!/bin/bash

echo "================================"
echo "Automated testing (MPI version)"
echo "================================"

# Переход в корень проекта
cd "$(dirname "$0")/.."

# Check executable
if [ ! -f "matrix_mult_mpi" ]; then
    echo "Error: matrix_mult_mpi not found!"
    echo "Run ./build.sh first."
    exit 1
fi

# Create data folder
mkdir -p data

# Generate test matrices
echo ""
echo "Generating test matrices (500x500)..."
python3 scripts/gen_matrix.py 500 data/input_A.txt
python3 scripts/gen_matrix.py 500 data/input_B.txt

# Test 1: Correctness check (4 processes)
echo ""
echo "Test 1: Correctness check (4 processes)"
echo "----------------------------------------"
mpiexec --oversubscribe -n 4 ./matrix_mult_mpi data/input_A.txt data/input_B.txt data/output_C.txt

if [ $? -ne 0 ]; then
    echo "Program execution error!"
    exit 1
fi

# Verification
python3 scripts/verify.py data/input_A.txt data/input_B.txt data/output_C.txt

if [ $? -ne 0 ]; then
    echo "VERIFICATION FAILED!"
    exit 1
fi

# Test 2: Different number of processes
echo ""
echo "Test 2: Different number of processes (with verification)"
echo "----------------------------------------"

# Используем --oversubscribe для запуска на любом числе процессов
for P in 1 2 4 8; do
    echo ""
    echo "Running on $P processes..."
    mpiexec --oversubscribe -n $P ./matrix_mult_mpi data/input_A.txt data/input_B.txt data/output_C.txt
    
    # Verification for each process count
    python3 scripts/verify.py data/input_A.txt data/input_B.txt data/output_C.txt
    
    if [ $? -ne 0 ]; then
        echo "VERIFICATION FAILED for $P processes!"
        exit 1
    fi
done

echo ""
echo "================================"
echo "ALL TESTS HAVE BEEN PASSED SUCCESSFULLY!"
echo "================================"
