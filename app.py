from flask import Flask, render_template, request, jsonify  # Import Flask modules for web app functionality
from sudokutools import valid, solve, find_empty, generate_board, generate_puzzle  # Import Sudoku-related utility functions
import random  # For generating random numbers
from copy import deepcopy  # To create deep copies of lists

# Create the Flask application instance
app = Flask(__name__)

def generate_sudoku_board():
    """Generates a fully solved Sudoku board using a backtracking solver."""
    board = [[0 for _ in range(9)] for _ in range(9)]  # Initialize a 9x9 board with zeros

    def is_safe(board, row, col, num):
        """Checks if placing a number is safe in a given row, column, and sub-grid."""
        if num in board[row]:  # Check if the number exists in the current row
            return False
        if num in [board[r][col] for r in range(9)]:  # Check if the number exists in the current column
            return False
        # Check if the number exists in the 3x3 sub-grid
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve(board):
        """Backtracking Sudoku solver."""
        for row in range(9):  # Iterate through all rows
            for col in range(9):  # Iterate through all columns
                if board[row][col] == 0:  # Find an empty cell
                    for num in range(1, 10):  # Try numbers 1 to 9
                        if is_safe(board, row, col, num):  # Check if it's safe to place the number
                            board[row][col] = num  # Place the number
                            if solve(board):  # Recursively solve the board
                                return True
                            board[row][col] = 0  # Reset the cell if the placement leads to failure
                    return False  # Return false if no number fits
        return True  # Return true if the board is solved

    solve(board)  # Solve the board to generate a full solution
    return board  # Return the solved board

def generate_puzzle(solved_board):
    """Generates a Sudoku puzzle by removing numbers from a solved board."""
    puzzle = [row[:] for row in solved_board]  # Create a copy of the solved board
    num_cells_to_remove = random.randint(40, 50)  # Randomly decide how many cells to remove
    for _ in range(num_cells_to_remove):  # Remove the specified number of cells
        row, col = random.randint(0, 8), random.randint(0, 8)  # Select a random cell
        puzzle[row][col] = 0  # Set the cell to 0 (empty)

    return puzzle  # Return the puzzle board

@app.route('/')
def index():
    # Render the index.html template for the home page
    return render_template('index.html')

@app.route('/generate', methods=['GET'])
def generate():
    # Generate a fully solved board
    solved_board = generate_sudoku_board()
    # Generate a puzzle by removing numbers from the solved board
    puzzle_board = generate_puzzle(solved_board)
    # Return the puzzle as JSON
    return jsonify(puzzle_board)

@app.route('/solve', methods=['POST'])
def solve_route():
    # Get the board data from the request JSON payload
    data = request.json
    board = data['board']
    # Solve the board using the solve function
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:  # Find empty cells
                solve(board)  # Solve the board (use your solver logic)
    # Return the solved board as JSON
    return jsonify(board)

@app.route('/hint', methods=['POST'])
def hint():
    # Get the board data and cell coordinates from the request
    data = request.json
    board = data['board']
    row = data['row']
    col = data['col']
    
    # Generate the solved board for providing hints
    solved_board = [row[:] for row in board]
    solve(solved_board)  # Solve the board to get the complete solution

    # Return the correct value for the requested cell if it is empty
    hint_value = solved_board[row][col] if board[row][col] == 0 else None
    return jsonify(hintValue=hint_value)

if __name__ == "__main__":
    # Run the Flask app in debug mode
    app.run(debug=True)
