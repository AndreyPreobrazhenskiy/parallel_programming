#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>
#include <cmath>
#include <string>
#include <chrono>
#include <mpi.h>

// Read matrix from file (1D array)
bool readMatrix(const std::string& filename, std::vector<double>& matrix, int& n) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error: Cannot open file " << filename << std::endl;
        return false;
    }
    file >> n;
    matrix.resize(n * n);
    for (int i = 0; i < n * n; ++i) {
        if (!(file >> matrix[i])) {
            std::cerr << "Error: Invalid data in " << filename << std::endl;
            return false;
        }
    }
    file.close();
    return true;
}

// Write matrix to file (1D array)
bool writeMatrix(const std::string& filename, const std::vector<double>& matrix, int n) {
    std::ofstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error: Cannot create file " << filename << std::endl;
        return false;
    }
    file << n << std::endl;
    file << std::fixed << std::setprecision(6);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            file << matrix[i * n + j] << " ";
        }
        file << std::endl;
    }
    file.close();
    return true;
}

// Sequential multiplication for a block of rows
void multiplyBlock(const std::vector<double>& A,
                   const std::vector<double>& B,
                   std::vector<double>& C,
                   int n, int start_row, int end_row) {
    for (int i = start_row; i < end_row; ++i) {
        for (int j = 0; j < n; ++j) {
            double sum = 0.0;
            for (int k = 0; k < n; ++k) {
                sum += A[i * n + k] * B[k * n + j];
            }
            C[i * n + j] = sum;
        }
    }
}

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);
    
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Broadcast file names
    std::string fileA, fileB, fileC;
    int arg_len;
    
    if (rank == 0) {
        if (argc < 4) {
            std::cout << "Usage: " << argv[0] << " <input_A> <input_B> <output_C>" << std::endl;
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
        fileA = argv[1];
        fileB = argv[2];
        fileC = argv[3];
    }
    
    arg_len = rank == 0 ? fileA.size() : 0;
    MPI_Bcast(&arg_len, 1, MPI_INT, 0, MPI_COMM_WORLD);
    if (rank != 0) fileA.resize(arg_len);
    MPI_Bcast(&fileA[0], arg_len, MPI_CHAR, 0, MPI_COMM_WORLD);
    
    arg_len = rank == 0 ? fileB.size() : 0;
    MPI_Bcast(&arg_len, 1, MPI_INT, 0, MPI_COMM_WORLD);
    if (rank != 0) fileB.resize(arg_len);
    MPI_Bcast(&fileB[0], arg_len, MPI_CHAR, 0, MPI_COMM_WORLD);
    
    arg_len = rank == 0 ? fileC.size() : 0;
    MPI_Bcast(&arg_len, 1, MPI_INT, 0, MPI_COMM_WORLD);
    if (rank != 0) fileC.resize(arg_len);
    MPI_Bcast(&fileC[0], arg_len, MPI_CHAR, 0, MPI_COMM_WORLD);

    // Rank 0 reads matrices
    int n = 0;
    std::vector<double> A, B, C;
    
    if (rank == 0) {
        std::cout << "Reading matrices..." << std::endl;
        if (!readMatrix(fileA, A, n)) {
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
        if (!readMatrix(fileB, B, n)) {
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
        C.resize(n * n);
        std::cout << "Matrix Size: " << n << "x" << n << std::endl;
        std::cout << "Processes: " << size << std::endl;
        std::cout << "Calculating..." << std::endl;
    }
    
    // Broadcast matrix size
    MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);
    
    // Allocate on all ranks
    if (rank != 0) {
        A.resize(n * n);
        B.resize(n * n);
        C.resize(n * n);
    }
    
    // Broadcast full matrices A and B to all processes
    MPI_Bcast(A.data(), n * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(B.data(), n * n, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    
    // Calculate rows per process
    int rows_per_proc = n / size;
    int remainder = n % size;
    int start_row = rank * rows_per_proc + std::min(rank, remainder);
    int end_row = start_row + rows_per_proc + (rank < remainder ? 1 : 0);
    int local_rows = end_row - start_row;
    
    // Local result buffer
    std::vector<double> C_local(n * n, 0.0);
    
    // Synchronize before timing
    MPI_Barrier(MPI_COMM_WORLD);
    auto start_time = std::chrono::high_resolution_clock::now();
    
    // Each process computes its block
    multiplyBlock(A, B, C_local, n, start_row, end_row);
    
    // Gather results to rank 0
    // Calculate displacements for irregular distribution
    std::vector<int> recv_counts(size);
    std::vector<int> displs(size);
    
    for (int p = 0; p < size; ++p) {
        int p_start = p * rows_per_proc + std::min(p, remainder);
        int p_end = p_start + rows_per_proc + (p < remainder ? 1 : 0);
        recv_counts[p] = (p_end - p_start) * n;
        displs[p] = p_start * n;
    }
    
    MPI_Gatherv(C_local.data() + start_row * n, recv_counts[rank], MPI_DOUBLE,
                C.data(), recv_counts.data(), displs.data(), MPI_DOUBLE, 0, MPI_COMM_WORLD);
    
    // Synchronize after computation
    MPI_Barrier(MPI_COMM_WORLD);
    auto end_time = std::chrono::high_resolution_clock::now();
    
    // Rank 0 outputs results
    if (rank == 0) {
        std::chrono::duration<double> elapsed = end_time - start_time;
        double flops = 2.0 * pow(n, 3);
        double gflops = flops / (elapsed.count() * 1e9);
        
        std::cout << "Time: " << elapsed.count() << " seconds" << std::endl;
        std::cout << "Performance: " << gflops << " GFLOPS" << std::endl;
        
        if (!writeMatrix(fileC, C, n)) {
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
        std::cout << "Result saved to " << fileC << std::endl;
        
        // Metrics for scripts
        std::cout << "METRIC:N:" << n << std::endl;
        std::cout << "METRIC:TIME:" << elapsed.count() << std::endl;
        std::cout << "METRIC:PROC:" << size << std::endl;
        std::cout << "METRIC:GFLOPS:" << gflops << std::endl;
    }
    
    MPI_Finalize();
    return 0;
}
