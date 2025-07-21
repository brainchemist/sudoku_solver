import cv2
import pytesseract
import numpy as np

# Path to tesseract executable (update if needed)
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Adjust if on Windows


def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    blur = cv2.GaussianBlur(img, (9, 9), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)
    return img, thresh


def find_largest_contour(thresh):
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    max_contour = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            max_contour = cnt
    return max_contour


def extract_grid(image, contour):
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    if len(approx) != 4:
        raise Exception("Couldn't find 4-corner Sudoku grid")

    approx = sorted(approx, key=lambda x: (x[0][1], x[0][0]))
    top = sorted(approx[:2], key=lambda x: x[0][0])
    bottom = sorted(approx[2:], key=lambda x: x[0][0])
    pts = np.array([top[0][0], top[1][0], bottom[1][0], bottom[0][0]], dtype='float32')

    side = max([
        np.linalg.norm(pts[0] - pts[1]),
        np.linalg.norm(pts[1] - pts[2]),
        np.linalg.norm(pts[2] - pts[3]),
        np.linalg.norm(pts[3] - pts[0])
    ])
    dst = np.array([[0, 0], [side-1, 0], [side-1, side-1], [0, side-1]], dtype='float32')
    M = cv2.getPerspectiveTransform(pts, dst)
    warp = cv2.warpPerspective(image, M, (int(side), int(side)))
    return warp


def extract_cells(grid_img):
    cells = []
    side = grid_img.shape[0] // 9
    for i in range(9):
        row = []
        for j in range(9):
            cell = grid_img[i * side:(i + 1) * side, j * side:(j + 1) * side]
            row.append(cell)
        cells.append(row)
    return cells


def clean_cell(cell_img):
    h, w = cell_img.shape
    margin = int(min(h, w) * 0.1)
    cell = cell_img[margin:h - margin, margin:w - margin]

    blur = cv2.GaussianBlur(cell, (5, 5), 0)
    _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Resize and invert for Tesseract
    digit = cv2.resize(binary, (60, 60), interpolation=cv2.INTER_LINEAR)
    digit = cv2.bitwise_not(digit)

    return digit


def recognize_digit(cell_img):
    digit_img = clean_cell(cell_img)
    config = '--psm 10 digits'
    text = pytesseract.image_to_string(digit_img, config=config)
    return int(text.strip()) if text.strip().isdigit() else 0


def board_from_cells(cells):
    board = []
    for row in cells:
        board_row = []
        for cell in row:
            digit = recognize_digit(cell)
            board_row.append(digit)
        board.append(board_row)
    return board


def save_board_to_file(board, filename="sudoku.txt"):
    with open(filename, "w") as f:
        for row in board:
            f.write(" ".join(str(x) for x in row) + "\n")


# Main routine
def process_sudoku_image(image_path):
    original, thresh = preprocess_image(image_path)
    contour = find_largest_contour(thresh)
    grid = extract_grid(original, contour)
    cells = extract_cells(grid)
    board = board_from_cells(cells)
    save_board_to_file(board)
    print("Board extracted and saved to sudoku.txt")

process_sudoku_image("sudoku_photo.jpg")