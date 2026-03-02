@echo off
setlocal enabledelayedexpansion

echo ================================
echo Full Benchmark Suite
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

:: Creating folders
if not exist "data" mkdir data

:: ========================================
:: FULL EXPERIMENT: All sizes x All threads
:: ========================================
echo.
echo Testing all combinations:
echo - Sizes: 200, 400, 800, 1000, 1200, 1600, 2000
echo - Threads: 1, 2, 4, 8
echo.

for %%N in (200 400 800 1000 1200 1600 2000) do (
    echo.
    echo ========================================
    echo Matrix Size: %%N x %%N
    echo ========================================
    
    :: Generate matrices once per size
    python scripts/gen_matrix.py %%N data/bench_A.txt
    python scripts/gen_matrix.py %%N data/bench_B.txt
    
    :: Measure on 1 thread (base for speedup)
    matrix_mult.exe data/bench_A.txt data/bench_B.txt data/bench_C.txt 1 > temp_output.txt 2>&1
    set BASE_TIME=
    for /f "tokens=3 delims=:" %%V in ('findstr "METRIC:TIME:" temp_output.txt') do set BASE_TIME=%%V
    set BASE_TIME=!BASE_TIME: =!
    
    echo.
    echo Threads    Time_sec    GFLOPS    Speedup
    echo --------    --------    ------    -------
    
    for %%T in (1 2 4 8) do (
        :: Run benchmark
        matrix_mult.exe data/bench_A.txt data/bench_B.txt data/bench_C.txt %%T > temp_output.txt 2>&1
        
        :: Parse time
        set CUR_TIME=
        for /f "tokens=3 delims=:" %%V in ('findstr "METRIC:TIME:" temp_output.txt') do set CUR_TIME=%%V
        set CUR_TIME=!CUR_TIME: =!
        
        :: Parse GFLOPS
        set GFLOPS_VAL=
        for /f "tokens=3 delims=:" %%G in ('findstr "METRIC:GFLOPS:" temp_output.txt') do set GFLOPS_VAL=%%G
        set GFLOPS_VAL=!GFLOPS_VAL: =!
        
        :: Calculate speedup
        set SPEEDUP=1.00
        if !BASE_TIME! NEQ 0 if !CUR_TIME! NEQ 0 (
            for /f %%S in ('python -c "print(round(!BASE_TIME! / !CUR_TIME!, 2))"') do set SPEEDUP=%%S
        )
        
        :: Display result
        echo    %%T        !CUR_TIME!      !GFLOPS_VAL!     !SPEEDUP!x
    )
)

:: Cleanup
del temp_output.txt 2>nul
del data\bench_A.txt 2>nul
del data\bench_B.txt 2>nul
del data\bench_C.txt 2>nul

echo.
echo ================================
echo All experiments completed!
echo ================================
pause