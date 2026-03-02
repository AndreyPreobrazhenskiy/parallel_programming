@echo off
echo ================================
echo Compilation of the program...
echo ================================

if not exist "src" (
    echo Error: The src folder was not found!
    pause
    exit /b 1
)

g++ -O3 -fopenmp -std=c++11 -o matrix_mult.exe src/main.cpp

if %errorlevel% neq 0 (
    echo Compilation error!
    pause
    exit /b 1
)

echo The compilation is successful!
echo ================================