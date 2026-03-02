#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>
#include <cmath>
#include <string>
#include <chrono>

// Function to read matrix from file
// Format: First line - size N, then N*N elements
bool readMatrix(const std::string& filename, std::vector<std::vector<double>>& matrix, int& n) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error: Cannot open file " << filename << std::endl;
        return false;
    }

    file >> n;
    matrix.resize(n, std::vector<double>(n));

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (!(file >> matrix[i][j])) {
                std::cerr << "Error: Invalid data in " << filename << std::endl;
                return false;
            }
        }
    }
    file.close();
    return true;
}

// Function to write matrix to file
bool writeMatrix(const std::string& filename, const std::vector<std::vector<double>>& matrix, int n) {
    std::ofstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error: Cannot create file " << filename << std::endl;
        return false;
    }

    file << n << std::endl;
    file << std::fixed << std::setprecision(6);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            file << matrix[i][j] << " ";
        }
        file << std::endl;
    }
    file.close();
    return true;
}

// Sequential matrix multiplication
// C = A * B
void multiplyMatrices(const std::vector<std::vector<double>>& A,
    const std::vector<std::vector<double>>& B,
    std::vector<std::vector<double>>& C,
    int n) {
    
    // Initialize with zeros and multiply
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            C[i][j] = 0.0;
            for (int k = 0; k < n; ++k) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc < 4) {
        std::cout << "Usage: " << argv[0] << " <input_A> <input_B> <output_C>" << std::endl;
        return 1;
    }

    std::string fileA = argv[1];
    std::string fileB = argv[2];
    std::string fileC = argv[3];

    std::vector<std::vector<double>> A, B, C;
    int nA, nB;

    std::cout << "Reading matrices..." << std::endl;
    if (!readMatrix(fileA, A, nA)) return 1;
    if (!readMatrix(fileB, B, nB)) return 1;

    if (nA != nB) {
        std::cerr << "Error: Matrices must be square and of same size." << std::endl;
        return 1;
    }
    int n = nA;

    C.resize(n, std::vector<double>(n));

    std::cout << "Matrix Size: " << n << "x" << n << std::endl;
    std::cout << "Calculating..." << std::endl;

    // Time measurement using chrono
    auto start_time = std::chrono::high_resolution_clock::now();

    multiplyMatrices(A, B, C, n);

    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end_time - start_time;

    // Computational volume (FLOPS): 2 * N^3 (multiplication + addition)
    double flops = 2.0 * pow(n, 3);
    double gflops = flops / (elapsed.count() * 1e9);

    std::cout << "Time: " << elapsed.count() << " seconds" << std::endl;
    std::cout << "Performance: " << gflops << " GFLOPS" << std::endl;

    if (!writeMatrix(fileC, C, n)) return 1;

    std::cout << "Result saved to " << fileC << std::endl;

    // Output metrics in parseable format (for scripts)
    std::cout << "METRIC:N:" << n << std::endl;
    std::cout << "METRIC:TIME:" << elapsed.count() << std::endl;
    std::cout << "METRIC:GFLOPS:" << gflops << std::endl;

    return 0;
}