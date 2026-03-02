import numpy as np
import sys


def read_matrix(filename):
    with open(filename, 'r') as f:
        n = int(f.readline())
        matrix = []
        for _ in range(n):
            row = list(map(float, f.readline().split()))
            matrix.append(row)
        return np.array(matrix)


def main():
    if len(sys.argv) != 4:
        print("Usage: python verify.py <input_A> <input_B> <output_C_cpp>")
        sys.exit(1)

    file_a = sys.argv[1]
    file_b = sys.argv[2]
    file_c_cpp = sys.argv[3]

    try:
        A = read_matrix(file_a)
        B = read_matrix(file_b)
        C_cpp = read_matrix(file_c_cpp)

        # Эталонный расчет на Python
        C_ref = np.dot(A, B)

        # Сравнение с учетом погрешности float
        if np.allclose(C_cpp, C_ref, rtol=1e-5, atol=1e-8):
            print("VERIFICATION: SUCCESS")
            print(f"Max difference: {np.max(np.abs(C_cpp - C_ref))}")
        else:
            print("VERIFICATION: FAILED")
            print(f"Max difference: {np.max(np.abs(C_cpp - C_ref))}")
            sys.exit(1)

    except Exception as e:
        print(f"VERIFICATION: ERROR - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()