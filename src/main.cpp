#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>
#include <omp.h>
#include <cmath>
#include <string>

// Функция чтения матрицы из файла
// Формат: Первая строка - размер N, далее N*N элементов
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

// Функция записи матрицы в файл
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

// Параллельное умножение матриц
// C = A * B
void multiplyMatrices(const std::vector<std::vector<double>>& A,
    const std::vector<std::vector<double>>& B,
    std::vector<std::vector<double>>& C,
    int n, int num_threads) {
    // Инициализация нулями
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            C[i][j] = 0.0;
        }
    }

    // Установка количества потоков
    omp_set_num_threads(num_threads);

    // Параллельная область
    // Порядок циклов i, k, j выбран для оптимизации кэш-памяти (доступ к B последовательный)
#pragma omp parallel for schedule(static)
    for (int i = 0; i < n; ++i) {
        for (int k = 0; k < n; ++k) {
            double a_ik = A[i][k];
            for (int j = 0; j < n; ++j) {
                C[i][j] += a_ik * B[k][j];
            }
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc < 4) {
        std::cout << "Usage: " << argv[0] << " <input_A> <input_B> <output_C> [threads]" << std::endl;
        return 1;
    }

    std::string fileA = argv[1];
    std::string fileB = argv[2];
    std::string fileC = argv[3];
    int num_threads = 4; // По умолчанию

    if (argc >= 5) {
        num_threads = std::atoi(argv[4]);
    }

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
    std::cout << "Threads: " << num_threads << std::endl;
    std::cout << "Calculating..." << std::endl;

    // Замер времени
    double start_time = omp_get_wtime();

    multiplyMatrices(A, B, C, n, num_threads);

    double end_time = omp_get_wtime();
    double elapsed = end_time - start_time;

    // Объем вычислений (FLOPS): 2 * N^3 (умножение + сложение)
    double flops = 2.0 * pow(n, 3);
    double gflops = flops / (elapsed * 1e9);

    std::cout << "Time: " << elapsed << " seconds" << std::endl;
    std::cout << "Performance: " << gflops << " GFLOPS" << std::endl;

    if (!writeMatrix(fileC, C, n)) return 1;

    std::cout << "Result saved to " << fileC << std::endl;

    // Вывод метрик в формате, удобном для парсинга (опционально для скриптов)
    std::cout << "METRIC:N:" << n << std::endl;
    std::cout << "METRIC:TIME:" << elapsed << std::endl;
    std::cout << "METRIC:THREADS:" << num_threads << std::endl;

    return 0;
}