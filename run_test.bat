@echo off
setlocal enabledelayedexpansion

echo ================================
echo Automated testing (Large Matrices)
echo ================================

:: Проверка наличия исполняемого файла
if not exist "matrix_mult.exe" (
    echo No executable file found. Starting compilation...
    call build.bat
    if !errorlevel! neq 0 exit /b 1
)

:: Создание папки data, если нет
if not exist "data" mkdir data

:: Генерация больших матриц (500x500)
echo.
echo Generating large matrices (500x500)...
python scripts/gen_matrix.py 500 data/input_A.txt
python scripts/gen_matrix.py 500 data/input_B.txt

echo.
echo Test 1: Correctness check (4 threads)
echo ----------------------------------------
matrix_mult.exe data/input_A.txt data/input_B.txt data/output_C.txt 4
if !errorlevel! neq 0 (
    echo Program execution error!
    pause
    exit /b 1
)

python scripts/verify.py data/input_A.txt data/input_B.txt data/output_C.txt
if !errorlevel! neq 0 (
    echo VERIFICATION FAILED!
    pause
    exit /b 1
)

echo.
echo Test 2: Different number of threads
echo ----------------------------------------
for %%T in (1 2 4 8) do (
    echo.
    echo Running on %%T threads...
    matrix_mult.exe data/input_A.txt data/input_B.txt data/output_C.txt %%T
)

echo.
echo ================================
echo ALL TESTS HAVE BEEN PASSED SUCCESSFULLY!
echo ================================
pause