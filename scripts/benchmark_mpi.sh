#!/bin/bash

echo "================================"
echo "MPI Benchmark Suite"
echo "================================"

# Переход в корень проекта
cd "$(dirname "$0")/.."

# Check executable
if [ ! -f "matrix_mult_mpi" ]; then
    echo "Error: matrix_mult_mpi not found!"
    exit 1
fi

# Create folders
mkdir -p results data

# CSV header
echo "N,Procs,Time,GFLOPS,Speedup" > results/mpi_results.csv

# Test different sizes
for N in 200 400 800 1000 1200 1600 2000; do
    echo ""
    echo "========================================"
    echo "Matrix Size: ${N}x${N}"
    echo "========================================"
    
    # Generate matrices
    python3 scripts/gen_matrix.py $N data/mpi_A.txt
    python3 scripts/gen_matrix.py $N data/mpi_B.txt
    
    # Get base time (1 process)
    mpiexec --oversubscribe -n 1 ./matrix_mult_mpi data/mpi_A.txt data/mpi_B.txt data/mpi_C.txt > /tmp/out.txt 2>&1
    BASE_TIME=$(grep "METRIC:TIME:" /tmp/out.txt | cut -d: -f3)
    
    echo "Procs | Time | GFLOPS | Speedup"
    echo "------+-------+--------+--------"
    
    for P in 1 2 4 8; do
        mpiexec --oversubscribe -n $P ./matrix_mult_mpi data/mpi_A.txt data/mpi_B.txt data/mpi_C.txt > /tmp/out.txt 2>&1
        
        TIME=$(grep "METRIC:TIME:" /tmp/out.txt | cut -d: -f3)
        GFLOPS=$(grep "METRIC:GFLOPS:" /tmp/out.txt | cut -d: -f3)
        SPEEDUP=$(python3 -c "print(round($BASE_TIME / $TIME, 2))")
        
        printf "  %d  | %.4f | %6.2f | %.2fx\n" $P $TIME $GFLOPS $SPEEDUP
        echo "$N,$P,$TIME,$GFLOPS,$SPEEDUP" >> results/mpi_results.csv
    done
done

echo ""
echo "================================"
echo "MPI Benchmark completed!"
echo "Results: results/mpi_results.csv"
echo "================================"
