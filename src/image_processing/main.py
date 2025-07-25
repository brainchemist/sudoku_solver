import requests
from dotenv import load_dotenv
import os
import subprocess

load_dotenv()

import re


def process_and_solve_sudoku(image_path):
    try:
        print(f"Processing image: {image_path}")
        RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
        RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST')

        url = f"https://{RAPIDAPI_HOST}/scan-puzzle"

        headers = {
            'x-rapidapi-host': RAPIDAPI_HOST,
            'x-rapidapi-key': RAPIDAPI_KEY
        }

        with open(image_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200:
            data = response.json()

            puzzle = []
            for row in data['puzzle']['rows']:
                puzzle_row = []
                for cell in row['cells']:
                    if cell['cell_type'] == 'solved':
                        puzzle_row.append(cell['value'])
                    else:
                        puzzle_row.append(0)
                puzzle.append(puzzle_row)

            write_sudoku_to_file(puzzle)

            sudoku_executable = os.path.abspath(os.path.join(os.path.dirname(__file__), '../solver/sudoku'))

            if not os.path.isfile(sudoku_executable):
                print(f"Error: {sudoku_executable} does not exist.")
                return f"Error: {sudoku_executable} does not exist."

            result = subprocess.run([sudoku_executable, "-f", "sudoku_puzzle.txt"], capture_output=True, text=True)


            if result.returncode == 0:
                solution = result.stdout.strip()

                clean_solution = remove_color_codes(solution)

                formatted_solution = format_sudoku_grid(clean_solution)
                return formatted_solution
            else:
                print(f"Error executing C program: {result.stderr.strip()}")
                return f"Error executing C program: {result.stderr.strip()}"

        else:
            print(f"OCR API error: {response.status_code}")
            return f"OCR API error: {response.status_code}"

    except Exception as e:
        print(f"Error in process_and_solve_sudoku: {str(e)}")
        return f"Error: {str(e)}"


def remove_color_codes(text):
    return re.sub(r'\x1b\[[0-9;]*m', '', text)


def format_sudoku_grid(solution):
    rows = solution.split("\n")
    formatted_grid = "+-------+-------+-------+\n"

    for i, row in enumerate(rows):
        row_values = row.split()
        formatted_grid += "| " + " ".join(row_values[:3]) + " | " + " ".join(row_values[3:6]) + " | " + " ".join(
            row_values[6:]) + " |\n"
        if (i + 1) % 3 == 0:
            formatted_grid += "+-------+-------+-------+\n"

    return formatted_grid


def write_sudoku_to_file(puzzle, filename="sudoku_puzzle.txt"):
    with open(filename, "w") as f:
        for row in puzzle:
            f.write(" ".join(str(x) for x in row) + "\n")
