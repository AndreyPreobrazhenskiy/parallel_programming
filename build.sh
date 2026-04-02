#!/bin/bash
echo "================================"
echo "Compiling MPI version..."
echo "================================"

mpicxx -O3 -std=c++11 -o matrix_mult_mpi src/main_mpi.cpp

if [ $? -ne 0 ]; then
    echo "Compilation failed!"
    exit 1
fi

echo "Compilation successful!"
echo "Executable: matrix_mult_mpi"
echo "================================"
