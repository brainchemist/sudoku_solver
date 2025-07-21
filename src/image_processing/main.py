import requests
from dotenv import load_dotenv
import os

load_dotenv()

RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST')

url = f"https://{RAPIDAPI_HOST}/scan-puzzle"

headers = {
    'x-rapidapi-host': RAPIDAPI_HOST,
    'x-rapidapi-key': RAPIDAPI_KEY
}

files = {'file': open('../../data/sudoku_photo.jpg', 'rb')} 

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


    def write_sudoku_to_file(puzzle, filename="sudoku_puzzle.txt"):
        with open(filename, "w") as f:
            for row in puzzle:
                f.write(" ".join(str(x) for x in row) + "\n")


    write_sudoku_to_file(puzzle)
    print("Sudoku puzzle has been written to sudoku_puzzle.txt")

else:
    print(f"Error {response.status_code}: {response.text}")

files['file'].close()
