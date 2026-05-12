#!/bin/bash
#SBATCH --job-name=mpi_lab3_benchmark
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --time=02:00:00
#SBATCH --output=benchmark_%j.out
#SBATCH --error=benchmark_%j.err

# Загрузить модули
module load intel/mpi4
module load intel/icc18

# Перейти в директорию
cd $SLURM_SUBMIT_DIR

echo "=== MPI Benchmark Started ==="
echo "Time: $(date)"
echo "Node: $(hostname)"

# Создать папку результатов
mkdir -p results
echo "N,Procs,Time,GFLOPS,Speedup" > results/mpi_results.csv

# Тест разных размеров
for N in 200 400 800 1000; do
    echo ""
    echo "=== Matrix Size: ${N}x${N} ==="
    
    # Генерация матриц
    python3 scripts/gen_matrix.py $N data/bench_A.txt
    python3 scripts/gen_matrix.py $N data/bench_B.txt
    
    # Базовое время (1 процесс)
    srun -n 1 ./matrix_mult_mpi data/bench_A.txt data/bench_B.txt data/bench_C.txt > /tmp/out.txt 2>&1
    BASE_TIME=$(grep "METRIC:TIME:" /tmp/out.txt | cut -d: -f3)
    
    echo "Procs | Time | GFLOPS | Speedup"
    echo "------+-------+--------+--------"
    
    for P in 1 2 4 8; do
        srun -n $P ./matrix_mult_mpi data/bench_A.txt data/bench_B.txt data/bench_C.txt > /tmp/out.txt 2>&1
        
        TIME=$(grep "METRIC:TIME:" /tmp/out.txt | cut -d: -f3)
        GFLOPS=$(grep "METRIC:GFLOPS:" /tmp/out.txt | cut -d: -f3)
        
        if [ -n "$BASE_TIME" ] && [ -n "$TIME" ]; then
            SPEEDUP=$(echo "scale=2; $BASE_TIME / $TIME" | bc 2>/dev/null || echo "N/A")
        else
            SPEEDUP="N/A"
        fi
        
        printf "  %d  | %.4f | %6.2f | %s\n" $P $TIME $GFLOPS $SPEEDUP
        echo "$N,$P,$TIME,$GFLOPS,$SPEEDUP" >> results/mpi_results.csv
    done
done

echo ""
echo "=== Benchmark Completed ==="
echo "Results saved to: results/mpi_results.csv"