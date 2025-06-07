import random  # Import the random module for generating random numbers

def valid(board, pos, num):
    """
    Checks if a number can be placed at the given position on the Sudoku board.
    Parameters:
        board (list): The 9x9 Sudoku board.
        pos (tuple): A tuple (row, col) indicating the position to check.
        num (int): The number to place.
    Returns:
        bool: True if the number can be placed, False otherwise.
    """
    row, col = pos  # Unpack the position tuple into row and column

    # Check the row for duplicates
    if num in board[row]:
        return False

    # Check the column for duplicates
    for i in range(9):
        if board[i][col] == num:
            return False

    # Check the 3x3 subgrid for duplicates
    start_row, start_col = row // 3 * 3, col // 3 * 3  # Find the top-left corner of the subgrid
    for i in range(3):  # Iterate over rows in the subgrid
        for j in range(3):  # Iterate over columns in the subgrid
            if board[start_row + i][start_col + j] == num:
                return False

    return True  # Return True if the number can be placed

def solve(board):
    """
    Solves the Sudoku board using backtracking.
    Parameters:
        board (list): The 9x9 Sudoku board.
    Returns:
        bool: True if the board is solved, False otherwise.
    """
    empty = find_empty(board)  # Find an empty cell
    if not empty:  # If no empty cell is found, the board is solved
        return True

    row, col = empty  # Unpack the position of the empty cell

    for num in range(1, 10):  # Try numbers from 1 to 9
        if valid(board, (row, col), num):  # Check if the number can be placed
            board[row][col] = num  # Place the number

            if solve(board):  # Recursively attempt to solve the board
                return True

            board[row][col] = 0  # Backtrack by resetting the cell to empty

    return False  # Return False if the board cannot be solved

def find_empty(board):
    """
    Finds an empty cell on the board. Empty cells are represented by 0.
    Parameters:
        board (list): The 9x9 Sudoku board.
    Returns:
        tuple or None: The position (row, col) of an empty cell, or None if no empty cells exist.
    """
    for i in range(9):  # Iterate through all rows
        for j in range(9):  # Iterate through all columns
            if board[i][j] == 0:  # Check if the cell is empty
                return (i, j)  # Return the position of the empty cell

    return None  # Return None if no empty cells are found

def generate_board():
    """
    Generates a random solved Sudoku board using backtracking.
    Returns:
        list: A fully solved 9x9 Sudoku board.
    """
    board = [[0 for _ in range(9)] for _ in range(9)]  # Create an empty 9x9 board filled with zeros
    solve(board)  # Solve the board to create a completed Sudoku

    return board  # Return the solved board

def generate_puzzle(solved_board):
    """
    Generates a Sudoku puzzle by removing numbers from a solved board.
    Parameters:
        solved_board (list): A fully solved 9x9 Sudoku board.
    Returns:
        list: A Sudoku puzzle with some cells removed (set to 0).
    """
    puzzle = [row[:] for row in solved_board]  # Create a copy of the solved board to avoid modifying it
    num_cells_to_remove = random.randint(40, 50)  # Decide randomly how many cells to remove (40-50)

    for _ in range(num_cells_to_remove):  # Loop to remove the decided number of cells
        row, col = random.randint(0, 8), random.randint(0, 8)  # Randomly select a cell
        puzzle[row][col] = 0  # Remove the value in the selected cell (set it to 0)

    return puzzle  # Return the generated puzzle
