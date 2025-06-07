let board = Array.from(Array(9), () => Array(9).fill(0));
// Initializes a 9x9 board filled with zeros to represent an empty Sudoku puzzle.

let solvedBoard = Array.from(Array(9), () => Array(9).fill(0));
// Initializes another 9x9 board to store the solved version of the Sudoku puzzle.

let timer;
// Variable to store the interval ID for the game timer.

let elapsedTime = 0;
// Tracks the elapsed time since the start of the game.

let musicPlaying = true;
// Boolean variable to track whether the background music is playing.

let wrong = 0;
// Variable to track the number of incorrect attempts (if needed).

let selectedCell = null;
// Variable to keep track of the currently selected cell on the board.

document.getElementById('generate').addEventListener('click', generateSudoku);
// Adds a click event listener to the "Generate" button to trigger the `generateSudoku` function.

document.getElementById('solve').addEventListener('click', solveSudoku);
// Adds a click event listener to the "Solve" button to trigger the `solveSudoku` function.

document.getElementById('reset').addEventListener('click', resetGame);
// Adds a click event listener to the "Reset" button to trigger the `resetGame` function.

document.getElementById('hint').addEventListener('click', giveHint);
// Adds a click event listener to the "Hint" button to trigger the `giveHint` function.

document.getElementById('music').addEventListener('click', toggleMusic);
// Adds a click event listener to the "Music" button to trigger the `toggleMusic` function.

function generateSudoku() {
    // Fetches a new Sudoku puzzle from the server and displays it.
    fetch('/generate')
        .then(response => response.json())
        // Converts the server response to JSON format.
        .then(data => {
            board = data;  // Updates the board with the fetched puzzle.
            fillBoard();   // Renders the board on the UI.
            startTimer();  // Starts the game timer.
        });
}

function fillBoard() {
    // Fills the board UI with the current state of the `board` variable.
    const boardDiv = document.getElementById('sudoku-board');
    boardDiv.innerHTML = '';  // Clears any existing board in the UI.

    for (let i = 0; i < 9; i++) {
        const rowDiv = document.createElement('div');
        // Creates a div to represent a row.

        rowDiv.className = 'row';
        // Assigns the class name "row" for styling.

        for (let j = 0; j < 9; j++) {
            const cell = document.createElement('input');
            // Creates an input element to represent a cell.

            cell.type = 'text';
            // Sets the input type to text.

            cell.maxLength = 1;
            // Limits input length to 1 character.

            cell.value = board[i][j] !== 0 ? board[i][j] : '';
            // Displays the cell value if it’s not zero, otherwise leaves it empty.

            cell.dataset.row = i;
            cell.dataset.col = j;
            // Stores the cell’s row and column as custom attributes.

            if (board[i][j] !== 0) {
                cell.disabled = true;
                // Disables editing for pre-filled cells.
            }

            cell.addEventListener('input', (e) => {
                // Validates the input to only allow numbers 1-9.
                const value = e.target.value;
                if (!/^[1-9]$/.test(value)) {
                    e.target.value = '';
                } else {
                    board[i][j] = parseInt(value);
                }
            });

            cell.addEventListener('focus', (e) => {
                // Updates the selected cell when a cell is focused.
                selectedCell = { row: i, col: j };
            });

            rowDiv.appendChild(cell);
            // Appends the cell to the row.
        }
        boardDiv.appendChild(rowDiv);
        // Appends the row to the board.
    }
}

function solveSudoku() {
    // Solves the current Sudoku puzzle by sending it to the server.
    fetch('/solve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ board })
    })
    .then(response => response.json())
    .then(data => {
        solvedBoard = data; // Updates the solved board.
        board = data; // Updates the current board to the solved board.
        fillBoard(); // Displays the solved board.
        stopTimer(); // Stops the timer since the game is solved.
    });
}

function giveHint() {
    // Provides a hint for the currently selected cell.
    if (selectedCell) {
        const row = selectedCell.row;
        const col = selectedCell.col;

        fetch('/hint', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ board, row, col })
        })
        .then(response => response.json())
        .then(data => {
            if (data.hintValue !== null) {
                const boardDiv = document.getElementById('sudoku-board');
                const inputCell = boardDiv.querySelector(`input[data-row='${row}'][data-col='${col}']`);
                inputCell.value = data.hintValue; // Displays the hint in the cell.
                board[row][col] = data.hintValue; // Updates the board with the hint value.
            } else {
                alert('No hint available for this cell!');
                // Alerts the user if a hint is not available.
            }
        });
    } else {
        alert('Please select a cell first!');
        // Alerts the user if no cell is selected.
    }
}

function resetGame() {
    // Resets the game board and timer.
    board = Array.from(Array(9), () => Array(9).fill(0));
    fillBoard();
    resetTimer();
}

function toggleMusic() {
    // Toggles the background music on or off.
    const music = document.getElementById('background-music');
    if (musicPlaying) {
        music.pause();
        musicPlaying = false;
    } else {
        music.play();
        musicPlaying = true;
    }
}

function startTimer() {
    // Starts the game timer.
    elapsedTime = 0;
    timer = setInterval(() => {
        elapsedTime++;
        document.getElementById('timer').innerText = `Time: ${elapsedTime}s`;
        // Updates the timer display every second.
    }, 1000);
}

function stopTimer() {
    // Stops the game timer.
    clearInterval(timer);
}

function resetTimer() {
    // Resets the timer to zero.
    stopTimer();
    document.getElementById('timer').innerText = 'Time: 0s';
}
