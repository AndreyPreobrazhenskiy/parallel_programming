# Умножение матриц

## Описание
Программа на C++ для перемножения квадратных матриц. Автоматическая верификация через Python (NumPy).

---

## Структура проекта

| Файл | Назначение |
|------|------------|
| `src/main.cpp` | Основной код C++ (умножение матриц) |
| `scripts/verify.py` | Проверка результата через Python/NumPy |
| `scripts/gen_matrix.py` | Генерация тестовых матриц |
| `build.bat` | Компиляция программы |
| `scripts/test_verification.bat` | Верификация результата |
| `scripts/benchmark.bat` | Тест на производительность |
| `data/` | Папка для входных/выходных файлов |

---

## Входные данные (матрицы)

### Формат входных файлов

Матрицы хранятся в текстовых файлах в папке `data/`:
- `N` — размер матрицы (первая строка)
- `a_ij` — элементы матрицы (разделены пробелами)

Пример: `test_A.txt`, `test_B.txt` - создаются при помощи `scripts/gen_matrix.py` для выполнения тестов.

### Выходные данные (результат):

Результат умножения сохраняется в файл `test_C.txt`.

## Как проходят тесты и проверки
**1. Верификация корректности (`test_verification.bat`)**

Что делает:
- Создаёт тестовые матрицы 3×3, 100×100, 500×500
- Запускает `matrix_mult.exe` (исполняемый файл, который создаётся автоматически при компиляции исходного кода (`build.bat`))
- Сравнивает результат с эталоном (Python + NumPy)
- Выводит `VERIFICATION: SUCCESS` или `FAILED`

**2. Тест производительности (`benchmark.bat`)**

Что делает:
- Генерирует матрицы разных размеров (200, 400, 800, 1000, 1200, 1600, 2000)
- Запускает умножение
- Замеряет время и вычисляет GFLOPS
- Выводит результаты в консоль

**Метрики:**
- Time_sec — время выполнения (секунды)
- GFLOPS — производительность (миллиардов операций в секунду)

---

## Как запускать

### Полный цикл (компиляция + тесты)
```cmd
build.bat
scripts\test_verification.bat
scripts\benchmark.bat
```

P.S. **Обязательно** иметь на компьютере **MinGW-w64 (g++)** для компиляции.

---

## Результаты

### Вывод `test_verification.bat`

```cmd
================================
Verification Test
================================

[Test 1] Small matrix (3x3)
----------------------------------------
Reading matrices...
Matrix Size: 3x3
Calculating...
Time: 0 seconds
Performance: inf GFLOPS
Result saved to data/test_C.txt
METRIC:N:3
METRIC:TIME:0
METRIC:GFLOPS:inf
Reading matrices...
Matrix A shape: (3, 3)
Matrix B shape: (3, 3)
Matrix C shape: (3, 3)
Calculating reference result...
Comparing results...
Max difference: 0.0
VERIFICATION: SUCCESS

[Test 2] Medium matrix (100x100)
----------------------------------------
Generated 100x100 matrix -> data/test_A.txt
Generated 100x100 matrix -> data/test_B.txt
Reading matrices...
Matrix Size: 100x100
Calculating...
Time: 0.0009974 seconds
Performance: 2.00521 GFLOPS
Result saved to data/test_C.txt
METRIC:N:100
METRIC:TIME:0.0009974
METRIC:GFLOPS:2.00521
Reading matrices...
Matrix A shape: (100, 100)
Matrix B shape: (100, 100)
Matrix C shape: (100, 100)
Calculating reference result...
Comparing results...
Max difference: 3.183231456205249e-12
VERIFICATION: SUCCESS

[Test 3] Large matrix (500x500)
----------------------------------------
Generated 500x500 matrix -> data/test_A.txt
Generated 500x500 matrix -> data/test_B.txt
Reading matrices...
Matrix Size: 500x500
Calculating...
Time: 0.134081 seconds
Performance: 1.86455 GFLOPS
Result saved to data/test_C.txt
METRIC:N:500
METRIC:TIME:0.134081
METRIC:GFLOPS:1.86455
Reading matrices...
Matrix A shape: (500, 500)
Matrix B shape: (500, 500)
Matrix C shape: (500, 500)
Calculating reference result...
Comparing results...
Max difference: 1.2732925824820995e-11
VERIFICATION: SUCCESS

================================
ALL VERIFICATION TESTS PASSED
================================
```











