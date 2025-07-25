from flask import Flask, request, jsonify, render_template, send_file
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os
import subprocess
import base64
import sys
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from image_processing.main import process_and_solve_sudoku

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/solve-sudoku', methods=['POST'])
def solve_sudoku():
    try:
        image_data = request.json['image']

        img_data = base64.b64decode(image_data.split(',')[1])
        img = Image.open(BytesIO(img_data))

        img.save('sudoku_image.jpg', 'JPEG')

        solution_output = process_and_solve_sudoku('sudoku_image.jpg')

        solution = parse_solution(solution_output)
        sudoku_solution_image_path = generate_sudoku_solution_image(solution)

        return jsonify({
            "image_url": "/static/solved_sudoku.png"
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

def generate_sudoku_solution_image(solution):
    cell_size = 50
    grid_size = cell_size * 9
    image = Image.new("RGB", (grid_size, grid_size), "white")
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    for row in range(9):
        for col in range(9):
            num = solution[row][col]
            x = col * cell_size
            y = row * cell_size
            text = str(num)

            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            text_x = x + (cell_size - text_width) // 2
            text_y = y + (cell_size - text_height) // 2
            draw.text((text_x, text_y), text, fill="black", font=font)

    for i in range(10):
        line_width = 3 if i % 3 == 0 else 1
        draw.line([(0, i * cell_size), (grid_size, i * cell_size)], fill="black", width=line_width)
        draw.line([(i * cell_size, 0), (i * cell_size, grid_size)], fill="black", width=line_width)

    print("Current Working Directory:", os.getcwd())

    image_path = "static/solved_sudoku.png"
    image.save(image_path)
    return image_path

def parse_solution(raw_output):
    lines = raw_output.splitlines()
    board = []
    for line in lines:
        if not any(char.isdigit() for char in line):
            continue

        numbers = [int(char) for char in line if char.isdigit()]
        if len(numbers) == 9:
            board.append(numbers)

    return board


if __name__ == '__main__':
    app.run(debug=True)
