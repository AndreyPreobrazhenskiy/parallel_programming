import sys
import random

if len(sys.argv) != 3:
    print("Usage: python gen_matrix.py <size> <filename>")
    sys.exit(1)

n = int(sys.argv[1])
filename = sys.argv[2]

with open(filename, 'w') as f:
    f.write(f"{n}\n")
    for i in range(n):
        row = [round(random.uniform(1, 10), 2) for _ in range(n)]
        f.write(" ".join(map(str, row)) + "\n")

print(f"Generated {n}x{n} matrix -> {filename}")