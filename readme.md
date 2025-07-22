
# Sudoku Solver with OCR Integration

This project processes an image of a Sudoku puzzle, extracts the puzzle using OCR, and then solves it using a C-based solver. The solution is executed via a Python script that interacts with both the OCR API and the C executable.

## Table of Contents

- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [License](#license)

## Project Structure

```
/CLionProjects/sudoku_solver/src/
├── image_processing
│   ├── main.py              # Main Python script to handle OCR, puzzle creation, and C program execution
│   ├── sudoku_photo.jpg     # Input Sudoku image
│   ├── sudoku_puzzle.txt    # Generated text file containing the Sudoku puzzle
│   └── sudoku.txt           # Placeholder text file (could be used for solving or debug purposes)
└── solver
├── main.c               # C program source code for solving the Sudoku puzzle
├── sudoku               # Compiled C executable for solving Sudoku
└── Makefile              # Build instructions for the C program (optional)
```

## Requirements

- **Python 3.x**
- **Libraries**:
  - `requests` for making API calls
  - `python-dotenv` for loading environment variables
  - `subprocess` for running the C program
- **C Compiler**:
  - A C compiler like `gcc` or `clang` to compile the C program.
- **Tesseract OCR**: To extract the puzzle from the image.

### Python Libraries

You can install the required Python libraries using `pip`:

```bash
pip install -r requirements.txt
```

### Install Tesseract OCR

Tesseract OCR is needed for extracting text from images. You can install it using the following commands:

#### On Ubuntu/Debian:

```bash
sudo apt install tesseract-ocr
```

#### On macOS (with Homebrew):

```bash
brew install tesseract
```

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/sudoku_solver.git
   cd sudoku_solver
   ```

2. **Create `.env` File**:
   In the `image_processing` directory, create a `.env` file with the following content:

   ```
   RAPIDAPI_KEY=your_rapidapi_key_here
   RAPIDAPI_HOST=sudoku-ocr.p.rapidapi.com
   ```

   Replace `your_rapidapi_key_here` with your actual API key from [RapidAPI](https://rapidapi.com/).

3. **Compile the C Program**:
   Navigate to the `solver` directory and compile the C program:

   ```bash
   gcc -o sudoku sudoku.c  # or use 'clang' if that's your preferred compiler
   ```

4. **Make Sure the Executable Has Permission**:
   Ensure that the `sudoku` executable has the correct permissions to execute:

   ```bash
   chmod +x solver/sudoku
   ```

## Usage

### 1. **Run the Python Script**:
Run the Python script from the `image_processing` directory:

```bash
python3 main.py
```

The script will:
- Upload the Sudoku image to the OCR API.
- Receive the extracted puzzle and generate a `sudoku_puzzle.txt` file.
- Pass the generated `sudoku_puzzle.txt` file to the C solver program (`sudoku`).
- Print the result from the C solver.

### 2. **Input Image**:
Place your Sudoku image in the `image_processing` directory as `sudoku_photo.jpg`. The script will automatically use this image for OCR.

### 3. **Solver Output**:
The C program will solve the Sudoku puzzle, and the output will be printed in the terminal.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

---

### Instructions:

1. **Markdown Syntax**: Copy the above content and save it as a `README.md` file in your project directory.
2. **Customization**: Replace the `your_rapidapi_key_here` with your actual API key in the `.env` section.

Let me know if you need anything else!