#include <stdio.h>
#include <stdbool.h>
#include <string.h>

#define SIZE 9

void printBoard(int board[SIZE][SIZE]) {
    for (int row = 0; row < SIZE; row++) {
        if (row % 3 == 0) printf("+-------+-------+-------+\n");
        for (int col = 0; col < SIZE; col++) {
            if (col % 3 == 0) printf("| ");
            if (board[row][col] == 0)
                printf("\033[1;31m. \033[0m");
            else
                printf("\033[1;32m%d \033[0m", board[row][col]);
        }
        printf("|\n");
    }
    printf("+-------+-------+-------+\n");
}


bool isValid(int board[SIZE][SIZE], int row, int col, int num) {
    for (int x = 0; x < SIZE; x++) {
        if (board[row][x] == num || board[x][col] == num)
            return false;
    }

    int startRow = row - row % 3;
    int startCol = col - col % 3;

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i + startRow][j + startCol] == num)
                return false;
        }
    }

    return true;
}

bool solveSudoku(int board[SIZE][SIZE]) {
    for (int row = 0; row < SIZE; row++) {
        for (int col = 0; col < SIZE; col++) {
            if (board[row][col] == 0) { // empty cell
                for (int num = 1; num <= 9; num++) {
                    if (isValid(board, row, col, num)) {
                        board[row][col] = num;

                        if (solveSudoku(board))
                            return true;

                        board[row][col] = 0; // backtrack
                    }
                }
                return false; // no valid number found
            }
        }
    }
    return true; // no empty cells left
}

bool readBoardFromFile(const char *filename, int board[SIZE][SIZE]) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        perror("Error opening file");
        return false;
    }

    for (int row = 0; row < SIZE; row++) {
        for (int col = 0; col < SIZE; col++) {
            if (fscanf(file, "%d", &board[row][col]) != 1) {
                fclose(file);
                fprintf(stderr, "Invalid format in file.\n");
                return false;
            }
        }
    }

    fclose(file);
    return true;
}

int main(int argc, char *argv[]) {
    int board[SIZE][SIZE];

    if (argc == 3 && strcmp(argv[1], "-f") == 0) {
        if (!readBoardFromFile(argv[2], board)) {
            return 1;
        }
    } else if (argc == 2 && strcmp(argv[1], "-i") == 0) {
        printf("Enter Sudoku board (9 lines of 9 numbers):\n");
        for (int row = 0; row < SIZE; row++) {
            for (int col = 0; col < SIZE; col++) {
                if (scanf("%d", &board[row][col]) != 1) {
                    fprintf(stderr, "Invalid input.\n");
                    return 1;
                }
            }
        }
    } else {
        // Invalid usage
        printf("Usage:\n");
        printf("  %s -f <filename>\tLoad board from file\n", argv[0]);
        printf("  %s -i\t\t\tEnter board manually\n", argv[0]);
        return 1;
    }

    printf("Input board:\n");
    printBoard(board);

    if (solveSudoku(board)) {
        printf("\nSolved board:\n");
        printBoard(board);
    } else {
        printf("\nNo solution exists.\n");
    }

    return 0;
}
