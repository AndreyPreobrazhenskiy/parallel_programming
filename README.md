# Умножение матриц с распараллеливанием (OpenMP)

## Описание
Программа на C++ для перемножения квадратных матриц с использованием OpenMP. Автоматическая верификация через Python (NumPy).

---

## Структура проекта

| Файл | Назначение |
|------|------------|
| `src/main.cpp` | Основной код C++ (умножение матриц + OpenMP) |
| `scripts/verify.py` | Проверка результата через Python/NumPy |
| `scripts/gen_matrix.py` | Генерация тестовых матриц |
| `build.bat` | Компиляция программы |
| `run_test.bat` | Верификация результата |
| `scripts/benchmark.bat` | Тесты на производительность |
| `data/` | Папка для входных/выходных файлов |

---

## Входные данные (матрицы)

### Формат входных файлов

Матрицы хранятся в текстовых файлах в папке `data/`:
- `N` — размер матрицы (первая строка)
- `a_ij` — элементы матрицы (разделены пробелами)

Пример: `input_A.txt`, `input_B.txt` - создаются при помощи `scripts/gen_matrix.py` для выполнения тестов.

### Выходные данные (результат):

Результат умножения сохраняется в файл `input_C.txt`.

---

## Как проходят тесты и проверки
**1. Верификация корректности (`run_test.bat`)**

Что делает:
- Создаёт тестовые матрицы 500×500
- Запускает умножение на 4 потоках
- Сравнивает результат с эталоном (Python + NumPy)
- Тестирует 1, 2, 4, 8 потоков
- При выполнении всех тестов выводит `ALL TESTS HAVE BEEN PASSED SUCCESSFULLY`

**2. Тест производительности (`benchmark.bat`)**

Что делает:
- Генерирует матрицы разных размеров (200, 400, 800, 1000, 1200, 1600, 2000)
- Запускает умножение для каждого размера: потоки 1, 2, 4, 8
- Выводит таблицу: `Threads` | `Time_sec` | `GFLOPS` | `Speedup`

**Метрики:**
- Time_sec — время выполнения (секунды)
- GFLOPS — производительность (миллиардов операций в секунду)
- Speedup — ускорение относительно 1 потока

---

## Как запускать

### Полный цикл (компиляция + тесты)
```cmd
build.bat && run_test.bat
scripts\benchmark.bat
```

P.S. **Обязательно** иметь на компьютере **MinGW-w64 (g++)** для компиляции.

---

## Результаты

### Вывод `run_test.bat`

```cmd
================================
Automated testing
================================

Generating large matrices (500x500)...
Generated 500x500 matrix -> data/input_A.txt
Generated 500x500 matrix -> data/input_B.txt

Test 1: Correctness check (4 threads)
----------------------------------------
Reading matrices...
Matrix Size: 500x500
Threads: 4
Calculating...
Time: 0.00900006 seconds
Performance: 27.7776 GFLOPS
Result saved to data/output_C.txt
METRIC:N:500
METRIC:TIME:0.00900006
METRIC:THREADS:4
METRIC:GFLOPS:27.7776
VERIFICATION: SUCCESS
Max difference: 1.0913936421275139e-11

Test 2: Different number of threads (with verification)
----------------------------------------

Running on 1 threads...
Reading matrices...
Matrix Size: 500x500
Threads: 1
Calculating...
Time: 0.039 seconds
Performance: 6.41025 GFLOPS
Result saved to data/output_C.txt
METRIC:N:500
METRIC:TIME:0.039
METRIC:THREADS:1
METRIC:GFLOPS:6.41025
VERIFICATION: SUCCESS
Max difference: 1.0913936421275139e-11

Running on 2 threads...
Reading matrices...
Matrix Size: 500x500
Threads: 2
Calculating...
Time: 0.0190001 seconds
Performance: 13.1579 GFLOPS
Result saved to data/output_C.txt
METRIC:N:500
METRIC:TIME:0.0190001
METRIC:THREADS:2
METRIC:GFLOPS:13.1579
VERIFICATION: SUCCESS
Max difference: 1.0913936421275139e-11

Running on 4 threads...
Reading matrices...
Matrix Size: 500x500
Threads: 4
Calculating...
Time: 0.0119998 seconds
Performance: 20.8336 GFLOPS
Result saved to data/output_C.txt
METRIC:N:500
METRIC:TIME:0.0119998
METRIC:THREADS:4
METRIC:GFLOPS:20.8336
VERIFICATION: SUCCESS
Max difference: 1.0913936421275139e-11

Running on 8 threads...
Reading matrices...
Matrix Size: 500x500
Threads: 8
Calculating...
Time: 0.0109999 seconds
Performance: 22.7274 GFLOPS
Result saved to data/output_C.txt
METRIC:N:500
METRIC:TIME:0.0109999
METRIC:THREADS:8
METRIC:GFLOPS:22.7274
VERIFICATION: SUCCESS
Max difference: 1.0913936421275139e-11

================================
ALL TESTS HAVE BEEN PASSED SUCCESSFULLY
================================
```

| Потоки | Время (с) | GFLOPS | Ускорение | Статус |
|--------|-----------|--------|-----------|--------|
| 1 | 0.039 | 6.41 | 1.00× | ✅ |
| 2 | 0.019 | 13.16 | 2.05× | ✅ |
| 4 | 0.012 | 20.83 | 3.25× | ✅ |
| 8 | 0.011 | 22.73 | 3.55× | ✅ |

> Все тесты пройдены. Ускорение на 8 потоках: **3.55×**. Эффективность снижается после 4 потоков из-за накладных расходов OpenMP (конкуренция за ресурсы памяти и закон Амдала). Оптимальное соотношение производительности и эффективности достигается при **2-4 потоках**.

---

### Вывод `benchmark.bat`

```cmd
================================
Full Benchmark Suite
================================

Testing all combinations:
- Sizes: 200, 400, 800, 1000, 1200, 1600, 2000
- Threads: 1, 2, 4, 8


========================================
Matrix Size: 200 x 200
========================================
Generated 200x200 matrix -> data/bench_A.txt
Generated 200x200 matrix -> data/bench_B.txt

Threads    Time_sec    GFLOPS    Speedup
--------    --------    ------    -------
   1        0.00199986      8.00058     1.0x
   2        0.00199986      8.00058     1.0x
   4        0.000999928      16.0012     2.0x
   8        0.000999928      16.0012     2.0x

========================================
Matrix Size: 400 x 400
========================================
Generated 400x400 matrix -> data/bench_A.txt
Generated 400x400 matrix -> data/bench_B.txt

Threads    Time_sec    GFLOPS    Speedup
--------    --------    ------    -------
   1        0.0189998      6.73691     1.0x
   2        0.0109999      11.6365     1.73x
   4        0.0059998      21.334     3.17x
   8        0.00499988      25.6006     3.8x

========================================
Matrix Size: 800 x 800
========================================
Generated 800x800 matrix -> data/bench_A.txt
Generated 800x800 matrix -> data/bench_B.txt

Threads    Time_sec    GFLOPS    Speedup
--------    --------    ------    -------
   1        0.179      5.72067     0.96x
   2        0.0899999      11.3778     1.9x
   4        0.05      20.48     3.42x
   8        0.036      28.4444     4.75x

========================================
Matrix Size: 1000 x 1000
========================================
Generated 1000x1000 matrix -> data/bench_A.txt
Generated 1000x1000 matrix -> data/bench_B.txt

Threads    Time_sec    GFLOPS    Speedup
--------    --------    ------    -------
   1        0.411      4.86618     1.0x
   2        0.207      9.66183     1.98x
   4        0.116      17.2414     3.53x
   8        0.0710001      28.169     5.77x

========================================
Matrix Size: 1200 x 1200
========================================
Generated 1200x1200 matrix -> data/bench_A.txt
Generated 1200x1200 matrix -> data/bench_B.txt

Threads    Time_sec    GFLOPS    Speedup
--------    --------    ------    -------
   1        0.786      4.39695     1.12x
   2        0.428      8.07477     2.07x
   4        0.253      13.6601     3.49x
   8        0.135      25.6     6.55x

========================================
Matrix Size: 1600 x 1600
========================================
Generated 1600x1600 matrix -> data/bench_A.txt
Generated 1600x1600 matrix -> data/bench_B.txt

Threads    Time_sec    GFLOPS    Speedup
--------    --------    ------    -------
   1        1.911      4.28676     1.03x
   2        1.095      7.48128     1.8x
   4        0.534      15.3408     3.7x
   8        0.379      21.6148     5.21x

========================================
Matrix Size: 2000 x 2000
========================================
Generated 2000x2000 matrix -> data/bench_A.txt
Generated 2000x2000 matrix -> data/bench_B.txt

Threads    Time_sec    GFLOPS    Speedup
--------    --------    ------    -------
   1        4.314      3.70885     0.98x
   2        2.679      5.97238     1.58x
   4        1.246      12.8411     3.4x
   8        0.759      21.0804     5.59x

================================
All experiments completed
================================
```

**Сводная таблица (производительность в GFLOPS)**

| Размер (N) | 1 поток | 2 потока | 4 потока | 8 потоков |
|------------|---------|----------|----------|-----------|
| 200 | 8.00 | 8.00 | 16.00 | 16.00 |
| 400 | 6.74 | 11.64 | 21.33 | 25.60 |
| 800 | 5.72 | 11.38 | 20.48 | 28.44 |
| 1000 | 4.87 | 9.66 | 17.24 | 28.17 |
| 1200 | 4.40 | 8.07 | 13.66 | 25.60 |
| 1600 | 4.29 | 7.48 | 15.34 | 21.61 |
| 2000 | 3.71 | 5.97 | 12.84 | 21.08 |

**Сводная таблица (ускорение, Speedup)**

| Размер (N) | 1 поток | 2 потока | 4 потока | 8 потоков |
|------------|---------|----------|----------|-----------|
| 200 | 1.0× | 1.0× | 2.0× | 2.0× |
| 400 | 1.0× | 1.73× | 3.17× | 3.80× |
| 800 | 0.96× | 1.90× | 3.42× | 4.75× |
| 1000 | 1.0× | 1.98× | 3.53× | 5.77× |
| 1200 | 1.12× | 2.07× | 3.49× | 6.55× |
| 1600 | 1.03× | 1.80× | 3.70× | 5.21× |
| 2000 | 0.98× | 1.58× | 3.40× | 5.59× |

---

### График зависимости времени выполнения от количества потоков:

<img width="2377" height="1478" alt="time_log_plot" src="https://github.com/user-attachments/assets/2d71c3f8-020a-4ee5-af46-b964a7b2b2ab" />


### График эффективности распараллеливания по размеру матрицы:

<img width="2982" height="1778" alt="speedup_plot" src="https://github.com/user-attachments/assets/fcc5fd5d-854e-4071-8114-b9301167df2a" />


### GFLOPS heatmap

<img width="2231" height="1479" alt="gflops_heatmap" src="https://github.com/user-attachments/assets/e2a414f2-5cd9-446a-8f7c-928eab06c765" />


> **Вывод:** Программа демонстрирует эффективное распараллеливание: ускорение растёт с увеличением числа потоков и размера матрицы. Для малых матриц (200×200) накладные расходы OpenMP нивелируют выгоду от многопоточности (ускорение ≤2×). Для больших матриц (≥1000) достигается ускорение **5.5–6.5×** на 8 потоках, что подтверждает масштабируемость алгоритма. Производительность в одиночном потоке снижается с ростом N (с 8.0 до 3.7 GFLOPS) из-за ограничений кэш-памяти и пропускной способности ОЗУ (memory-bound режим). Оптимальная эффективность достигается при **4–8 потоках** и размере матрицы **≥1000**.







