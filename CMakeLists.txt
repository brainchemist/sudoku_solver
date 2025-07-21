cmake_minimum_required(VERSION 3.31)
project(sudoku_solver C)

set(CMAKE_C_STANDARD 11)

add_executable(sudoku_solver main.c)

configure_file(${CMAKE_SOURCE_DIR}/sudoku.txt ${CMAKE_BINARY_DIR}/sudoku.txt COPYONLY)