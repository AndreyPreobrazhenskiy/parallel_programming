@echo off
setlocal enabledelayedexpansion

echo ================================
echo Benchmark
echo ================================

:: Check: must be run from project root
if not exist "matrix_mult.exe" (
    echo Error: matrix_mult.exe not found!
    echo Please run this script from the project root folder.
    pause
    exit /b 1
)

:: Checking dependencies
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Python was not found!
    pause
    exit /b 1
)

:: Creating data folder
if not exist "data" mkdir data

:: ========================================
:: EXPERIMENT: Different matrix sizes
:: ========================================
echo.
echo Testing different matrix sizes:
echo - Sizes: 200, 400, 800, 1000, 1200, 1600, 2000
echo.

for %%N in (200 400 800 1000 1200 1600 2000) do (
    echo.
    echo ========================================
    echo Matrix Size: %%N x %%N
    echo ========================================
    
    :: Generate matrices
    python scripts/gen_matrix.py %%N data/bench_A.txt
    python scripts/gen_matrix.py %%N data/bench_B.txt
    
    :: Run benchmark
    matrix_mult.exe data/bench_A.txt data/bench_B.txt data/bench_C.txt > temp_output.txt 2>&1
    
    :: Parse time
    set TIME_VAL=
    for /f "tokens=3 delims=:" %%V in ('findstr "METRIC:TIME:" temp_output.txt') do set TIME_VAL=%%V
    set TIME_VAL=!TIME_VAL: =!
    
    :: Parse GFLOPS
    set GFLOPS_VAL=
    for /f "tokens=3 delims=:" %%G in ('findstr "METRIC:GFLOPS:" temp_output.txt') do set GFLOPS_VAL=%%G
    set GFLOPS_VAL=!GFLOPS_VAL: =!
    
    :: Display result
    echo   Time: !TIME_VAL! sec
    echo   Performance: !GFLOPS_VAL! GFLOPS
)

:: Cleanup
del temp_output.txt 2>nul
del data\bench_A.txt 2>nul
del data\bench_B.txt 2>nul
del data\bench_C.txt 2>nul

echo.
echo ================================
echo Benchmark completed!
echo ================================
pause