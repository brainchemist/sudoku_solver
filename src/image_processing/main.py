import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Get the API key and host from environment variables
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST')

# API endpoint URL
url = f"https://{RAPIDAPI_HOST}/scan-puzzle"

# Your RapidAPI headers
headers = {
    'x-rapidapi-host': RAPIDAPI_HOST,
    'x-rapidapi-key': RAPIDAPI_KEY
}

# The image file you want to upload
files = {'file': open('../../data/sudoku_photo.jpg', 'rb')}  # Replace 'sudoku_image.jpg' with your actual file path

# Send the POST request with the image
response = requests.post(url, headers=headers, files=files)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Extract the puzzle rows and cells
    puzzle = []
    for row in data['puzzle']['rows']:
        puzzle_row = []
        for cell in row['cells']:
            if cell['cell_type'] == 'solved':
                puzzle_row.append(cell['value'])  # Add the value of solved cells
            else:
                puzzle_row.append(0)  # Use 0 for unsolved cells
        puzzle.append(puzzle_row)


    # Function to write the Sudoku puzzle to a text file in the desired format
    def write_sudoku_to_file(puzzle, filename="sudoku_puzzle.txt"):
        with open(filename, "w") as f:
            for row in puzzle:
                # Write each row as space-separated values
                f.write(" ".join(str(x) for x in row) + "\n")


    # Write the puzzle to a file
    write_sudoku_to_file(puzzle)
    print("Sudoku puzzle has been written to sudoku_puzzle.txt")

else:
    print(f"Error {response.status_code}: {response.text}")

# Close the file after use
files['file'].close()
