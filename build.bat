@echo off
echo ================================
echo Compiling the program...
echo ================================

if not exist "src" (
    echo Error: src folder not found!
    pause
    exit /b 1
)

:: No -fopenmp flag for sequential version
g++ -O3 -std=c++11 -o matrix_mult.exe src/main.cpp

if %errorlevel% neq 0 (
    echo Compilation failed!
    pause
    exit /b 1
)

echo Compilation successful!
echo ================================