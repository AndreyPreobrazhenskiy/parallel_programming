# Умножение матриц с распараллеливанием (MPI)

## Описание
Программа на C++ для перемножения квадратных матриц с использованием технологии MPI (Message Passing Interface). Автоматическая верификация результатов через Python (NumPy).

---

## Структура проекта

| Файл | Назначение |
|------|------------|
| `src/main_mpi.cpp` | Исходный код C++ (умножение матриц + MPI) |
| `scripts/verify.py` | Проверка результата через Python/NumPy |
| `scripts/gen_matrix.py` | Генерация тестовых матриц |
| `build.sh` | Компиляция программы (Linux) |
| `scripts/run_test.sh` | Автоматическая верификация |
| `scripts/benchmark_mpi.sh` | Серия экспериментов производительности |
| `scripts/plot_mpi.py` | Построение графиков (9 визуализаций) |
| `data/` | Папка для входных/выходных файлов | 
| `results/` | Папка для результатов бенчмарка и графиков |

---

## Входные данные (матрицы)

### Формат входных файлов

Матрицы хранятся в текстовых файлах в папке `data/`:
- `N` — размер матрицы (первая строка)
- `a_ij` — элементы матрицы (разделены пробелами)

Создаются при помощи `scripts/gen_matrix.py` для выполнения тестов.

## Как проходят тесты и проверки
**1. Верификация корректности (`run_test.sh`)**

Что делает:
- Создаёт тестовые матрицы 500×500
- Запускает `matrix_mult_mpi` на 1, 2, 4, 8 процессах
- Сравнивает результат с эталоном (Python + NumPy)
- Выводит `VERIFICATION: SUCCESS` или `FAILED`

**2. Тест производительности (`benchmark_mpi.sh`)**

Что делает:
- Генерирует матрицы размеров: 200, 400, 800, 1000, 1200, 1600, 2000
- Для каждого размера запускает умножение на 1, 2, 4, 8 процессах
- Замеряет время и вычисляет метрики: GFLOPS, Speedup, Efficiency
- Сохраняет результаты в `results/mpi_results.csv`

**Метрики:**
| Метрика | Описание | Формула | 
|------|--------|-------------|
| Time | Время выполнения (сек) | Замер через `std::chrono` | 
| GFLOPS | Производительность | `2×N³ / (Time × 10⁹)` | 
| Speedup | Ускорение | `T(1 proc) / T(N procs)` | 
| Efficiency | Эффективность | `Speedup / N × 100%` |

---

## Как запускать

### Полный цикл (компиляция + тесты)

**1. Компиляция**
```cmd
./build.sh
```

**2. Верификация корректности**
```cmd
./scripts/run_test.sh
```

**3. Бенчмарк производительности**
```cmd
./scripts/benchmark_mpi.sh
```

**4. Построение графиков**
```cmd
python3 scripts/plot_mpi.py
```

**Требования**:
- ОС: Linux (Ubuntu/Debian) или WSL2
- Компилятор: g++ или clang++
- MPI: openmpi-bin, libopenmpi-dev
- Python: 3.8+ с библиотеками numpy, pandas, matplotlib


**Установка зависимостей (Ubuntu)**:

```cmd
sudo apt install openmpi-bin libopenmpi-dev g++ python3 python3-pip
```

```cmd
sudo apt install python3-numpy python3-pandas python3-matplotlib
```

---

## Результаты

### Вывод `run_test.sh`

```cmd
================================
Automated testing (MPI version)
================================

Generating test matrices (500x500)...
Generated 500x500 matrix -> data/input_A.txt
Generated 500x500 matrix -> data/input_B.txt

Test 1: Correctness check (4 processes)
----------------------------------------
Reading matrices...
Matrix Size: 500x500
Processes: 4
Calculating...
Time: 0.0556987 seconds
Performance: 4.48844 GFLOPS
Result saved to data/output_C.txt
METRIC:N:500
METRIC:TIME:0.0556987
METRIC:PROC:4
METRIC:GFLOPS:4.48844
Reading matrices...
Matrix A shape: (500, 500)
Matrix B shape: (500, 500)
Matrix C shape: (500, 500)
Calculating reference result...
Comparing results...
Max difference: 3.8198777474462986e-11
VERIFICATION: SUCCESS

Test 2: Different number of processes (with verification)
----------------------------------------

Running on 1 processes...
Reading matrices...
Matrix Size: 500x500
Processes: 1
Calculating...
Time: 0.139586 seconds
Performance: 1.79101 GFLOPS
Result saved to data/output_C.txt
METRIC:N:500
METRIC:TIME:0.139586
METRIC:PROC:1
METRIC:GFLOPS:1.79101
Reading matrices...
Matrix A shape: (500, 500)
Matrix B shape: (500, 500)
Matrix C shape: (500, 500)
Calculating reference result...
Comparing results...
Max difference: 3.8198777474462986e-11
VERIFICATION: SUCCESS

Running on 2 processes...
Reading matrices...
Matrix Size: 500x500
Processes: 2
Calculating...
Time: 0.0785625 seconds
Performance: 3.18218 GFLOPS
Result saved to data/output_C.txt
METRIC:N:500
METRIC:TIME:0.0785625
METRIC:PROC:2
METRIC:GFLOPS:3.18218
Reading matrices...
Matrix A shape: (500, 500)
Matrix B shape: (500, 500)
Matrix C shape: (500, 500)
Calculating reference result...
Comparing results...
Max difference: 3.8198777474462986e-11
VERIFICATION: SUCCESS

Running on 4 processes...
Reading matrices...
Matrix Size: 500x500
Processes: 4
Calculating...
Time: 0.068179 seconds
Performance: 3.66682 GFLOPS
Result saved to data/output_C.txt
METRIC:N:500
METRIC:TIME:0.068179
METRIC:PROC:4
METRIC:GFLOPS:3.66682
Reading matrices...
Matrix A shape: (500, 500)
Matrix B shape: (500, 500)
Matrix C shape: (500, 500)
Calculating reference result...
Comparing results...
Max difference: 3.8198777474462986e-11
VERIFICATION: SUCCESS

Running on 8 processes...
Reading matrices...
Matrix Size: 500x500
Processes: 8
Calculating...
Time: 0.0792123 seconds
Performance: 3.15608 GFLOPS
Result saved to data/output_C.txt
METRIC:N:500
METRIC:TIME:0.0792123
METRIC:PROC:8
METRIC:GFLOPS:3.15608
Reading matrices...
Matrix A shape: (500, 500)
Matrix B shape: (500, 500)
Matrix C shape: (500, 500)
Calculating reference result...
Comparing results...
Max difference: 3.8198777474462986e-11
VERIFICATION: SUCCESS

================================
ALL TESTS HAVE BEEN PASSED SUCCESSFULLY!
================================
```


| Процессы | Время (сек) | Производительность (GFLOPS) | Ускорение | Погрешность | Статус |
|----------|-------------|----------------------------|-----------|-------------|--------|
| 1 | 0.1396 | 1.79 | 1.00× | 3.82×10⁻¹¹ | ✅ |
| 2 | 0.0786 | 3.18 | 1.78× | 3.82×10⁻¹¹ | ✅ |
| 4 | 0.0682 | 3.67 | 2.05× | 3.82×10⁻¹¹ | ✅ |
| 8 | 0.0792 | 3.16 | 1.76× | 3.82×10⁻¹¹ | ✅ |

> **Вывод:** Все тесты завершены со статусом `VERIFICATION: SUCCESS`. Максимальная погрешность `3.82×10⁻¹¹` находится в пределах машинной точности типа `double`. Оптимальное ускорение достигается при **4 процессах** (2.05×).

---

### Вывод `benchmark_mpi.sh`

```cmd
================================
MPI Benchmark Suite
================================

========================================
Matrix Size: 200x200
========================================
Generated 200x200 matrix -> data/mpi_A.txt
Generated 200x200 matrix -> data/mpi_B.txt
Procs | Time | GFLOPS | Speedup
------+-------+--------+--------
  1  | 0.0077 |   2.06 | 1.05x
  2  | 0.0043 |   3.73 | 1.89x
  4  | 0.0020 |   8.11 | 4.11x
  8  | 0.0031 |   5.11 | 2.59x

========================================
Matrix Size: 400x400
========================================
Generated 400x400 matrix -> data/mpi_A.txt
Generated 400x400 matrix -> data/mpi_B.txt
Procs | Time | GFLOPS | Speedup
------+-------+--------+--------
  1  | 0.0725 |   1.77 | 0.96x
  2  | 0.0354 |   3.62 | 1.96x
  4  | 0.0201 |   6.37 | 3.45x
  8  | 0.0288 |   4.45 | 2.41x

========================================
Matrix Size: 800x800
========================================
Generated 800x800 matrix -> data/mpi_A.txt
Generated 800x800 matrix -> data/mpi_B.txt
Procs | Time | GFLOPS | Speedup
------+-------+--------+--------
  1  | 0.7359 |   1.39 | 0.92x
  2  | 0.4431 |   2.31 | 1.54x
  4  | 0.2950 |   3.47 | 2.31x
  8  | 0.3242 |   3.16 | 2.10x

========================================
Matrix Size: 1000x1000
========================================
Generated 1000x1000 matrix -> data/mpi_A.txt
Generated 1000x1000 matrix -> data/mpi_B.txt
Procs | Time | GFLOPS | Speedup
------+-------+--------+--------
  1  | 2.7867 |   0.72 | 1.07x
  2  | 1.6089 |   1.24 | 1.85x
  4  | 0.9324 |   2.14 | 3.19x
  8  | 0.7500 |   2.67 | 3.97x

========================================
Matrix Size: 1200x1200
========================================
Generated 1200x1200 matrix -> data/mpi_A.txt
Generated 1200x1200 matrix -> data/mpi_B.txt
Procs | Time | GFLOPS | Speedup
------+-------+--------+--------
  1  | 4.0138 |   0.86 | 1.19x
  2  | 2.2472 |   1.54 | 2.12x
  4  | 1.2364 |   2.80 | 3.86x
  8  | 1.4220 |   2.43 | 3.36x

========================================
Matrix Size: 1600x1600
========================================
Generated 1600x1600 matrix -> data/mpi_A.txt
Generated 1600x1600 matrix -> data/mpi_B.txt
Procs | Time | GFLOPS | Speedup
------+-------+--------+--------
  1  | 25.7860 |   0.32 | 1.02x
  2  | 13.3101 |   0.62 | 1.97x
  4  | 8.0298 |   1.02 | 3.27x
  8  | 6.2131 |   1.32 | 4.23x

========================================
Matrix Size: 2000x2000
========================================
Generated 2000x2000 matrix -> data/mpi_A.txt
Generated 2000x2000 matrix -> data/mpi_B.txt
Procs | Time | GFLOPS | Speedup
------+-------+--------+--------
  1  | 99.2557 |   0.16 | 0.96x
  2  | 57.2441 |   0.28 | 1.67x
  4  | 25.9691 |   0.62 | 3.68x
  8  | 18.1272 |   0.88 | 5.27x

================================
MPI Benchmark completed!
Results: results/mpi_results.csv
================================
```

| Размер (N) | 1 поток (с) | 2 потока (с) | 4 потока (с) | 8 потоков (с) | 1 поток (GFLOPS) | 8 потоков (GFLOPS) | Speedup (8 proc) |
|------------|-------------|--------------|--------------|---------------|------------------|-------------------|------------------|
| 200 | 0.0077 | 0.0043 | 0.0020 | 0.0031 | 2.06 | 5.11 | 2.59× |
| 400 | 0.0725 | 0.0354 | 0.0201 | 0.0288 | 1.77 | 4.45 | 2.41× |
| 800 | 0.7359 | 0.4431 | 0.2950 | 0.3242 | 1.39 | 3.16 | 2.10× |
| 1000 | 2.7867 | 1.6089 | 0.9324 | 0.7500 | 0.72 | 2.67 | 3.97× |
| 1200 | 4.0138 | 2.2472 | 1.2364 | 1.4220 | 0.86 | 2.43 | 3.36× |
| 1600 | 25.7860 | 13.3101 | 8.0298 | 6.2131 | 0.32 | 1.32 | 4.23× |
| 2000 | 99.2557 | 57.2441 | 25.9691 | 18.1272 | 0.16 | 0.88 | 5.27× |

> **Вывод:** Ускорение растёт с увеличением размера матрицы. Для малых матриц (200–400) накладные расходы MPI снижают эффективность параллелизма. Для больших матриц (≥1000) достигается ускорение **3.4–5.3×** на 8 процессах. Производительность в одиночном потоке падает с ростом N (с 2.06 до 0.16 GFLOPS) из-за ограничений пропускной способности памяти.


### График 1: Parallel Speedup by Matrix Size (Ускорение)

<img width="2970" height="1766" alt="01_speedup_linear" src="https://github.com/user-attachments/assets/6be1ea07-145a-4e9c-9020-a1ae5c77de16" />



> **Вывод:** Ускорение растёт с увеличением размера матрицы. Для малых матриц (N=200-400) наблюдается падение ускорения при 8 процессах из-за накладных расходов MPI. Для больших матриц (N=1600-2000) достигается наилучшее ускорение 4.2–5.3× на 8 процессах, что подтверждает эффективность распараллеливания для больших задач.



### График 2: Performance by Matrix Size and Process Count (GFLOPS)

<img width="2970" height="1766" alt="02_gflops" src="https://github.com/user-attachments/assets/75464859-25f8-4815-9560-27fb1ba806d4" />



> **Вывод:** Пиковая производительность 8.11 GFLOPS достигается для малых матриц (N=200) на 4 процессах. Для больших матриц производительность снижается (0.88 GFLOPS для N=2000) из-за перехода в memory-bound режим — программа ограничивается пропускной способностью памяти, а не вычислительной мощностью.



### График 3: Performance Heatmap (GFLOPS)

<img width="2746" height="2067" alt="05_heatmap_gflops" src="https://github.com/user-attachments/assets/dea48ad2-a58a-4be2-b10f-9dea387dd8d6" />



> **Вывод:** Тепловая карта наглядно показывает, что оптимальная конфигурация — 4 процесса для малых и средних матриц (N=200-400). Для больших матриц (N≥1000) производительность плавно растёт с числом процессов, но остаётся низкой (< 3 GFLOPS). Самая тёмная ячейка (8.11 GFLOPS) — N=200, 4 процесса.



### График 4: Parallel Efficiency by Matrix Size (Эффективность)

<img width="2970" height="1766" alt="04_efficiency" src="https://github.com/user-attachments/assets/73e615e3-674e-41bd-ae09-4fb7c552315e" />



> **Вывод:** Эффективность снижается с ростом числа процессов (закон Амдала). Для N=2000 на 8 процессах эффективность составляет 66% — приемлемый результат. Для малых матриц (N=200-400) эффективность на 8 процессах падает до 25-32%, что указывает на доминирование накладных расходов коммуникации над выгодами параллелизма.



### График 5: Scaling with Matrix Size Log-Log (Масштабируемость)

<img width="2966" height="1759" alt="03_time_loglog" src="https://github.com/user-attachments/assets/005351b4-5845-4ca9-abf1-16f20340ef70" />



> **Вывод:** На логарифмическом масштабе видно, что время выполнения растёт пропорционально O(N³) (пунктирная линия), что соответствует теоретической сложности алгоритма умножения матриц. Параллельные версии (2, 4, 8 процессов) сохраняют ту же асимптотику, но с меньшими константами, что подтверждает корректность реализации и масштабируемость алгоритма.



### График 6: Performance vs Processes (N=1000)

<img width="2971" height="1766" alt="06_combined_n1000" src="https://github.com/user-attachments/assets/1553d9d1-d921-41c9-ae44-1873399f4d21" />



> **Вывод:** Для матрицы N=1000 наблюдается чёткая обратная зависимость: время выполнения снижается с 2.79с до 0.75с (в 3.7 раза), а производительность растёт с 0.72 до 2.67 GFLOPS (в 3.7 раза). Наибольший прирост достигается при переходе с 1 на 2 процесса (время уменьшается на 42%), что указывает на эффективное распараллеливание базовой нагрузки.



### График 7: Speedup Summary Table

<img width="3602" height="1168" alt="08_summary_table" src="https://github.com/user-attachments/assets/660f15ab-cfdb-44e2-aae3-04705ed04e37" />



> **Вывод:** Сводная таблица показывает, что максимальное ускорение 5.27× достигается для N=2000 на 8 процессах. Для малых матриц (N=200-400) ускорение на 8 процессах снижается (2.41–2.59×) из-за накладных расходов. Оптимальный баланс между размером задачи и количеством процессов: N≥1000 + 4-8 процессов.



### График 8: Strong Scaling Analysis (Fixed Problem Size)

<img width="4167" height="1541" alt="07_strong_scaling" src="https://github.com/user-attachments/assets/3dced6a7-efa1-4570-ab1c-e816944aab86" />



> **Вывод:** Анализ strong scaling показывает, что большая матрица (N=2000) масштабируется лучше: ускорение 5.27× против 3.97× для N=1000 на 8 процессах. Время выполнения для N=2000 снижается с 99с до 18с, что демонстрирует эффективность распараллеливания для вычислительно-ёмких задач. N=1000 упирается в ограничения памяти быстрее.



### График 9: MPI Performance Dashboard (4-в-1)

<img width="4167" height="3071" alt="09_dashboard" src="https://github.com/user-attachments/assets/f0c850b2-9acb-4adb-b204-74c55b9db83c" />



### Общий вывод: MPI-реализация эффективна для больших матриц (N≥1000) с 4-8 процессами. Малые матрицы не выигрывают от распараллеливания из-за накладных расходов коммуникации.
