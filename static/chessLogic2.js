document.addEventListener("DOMContentLoaded", function() {
    // Initialize the chessboard when the DOM is fully loaded
    createChessboardFromState();
    setInterval(updateChessboard, 200);  // Update the chessboard every 200ms
});

let firstClick = null;
const chessboardContainer = document.getElementById('chessboard-container');
const resetButton = document.getElementById('reset-button');
resetButton.addEventListener('click', handleResetClick);

// Function to create the chessboard based on the current state
function createChessboardFromState() {
    getBoardState(function(responseData){
        var spot_matrix = responseData["spot_matrix"];
        createResetChessboard(spot_matrix);
    });
}

// Function to clear all graphics from the chessboard container
function clearBoardGraphics() {
    chessboardContainer.innerHTML = '';  // Clear the entire content of the container
}

// Function to clear all images from the squares
function clearBoardImages() {
    var allSquares = document.querySelectorAll('.square');
    allSquares.forEach(square => {
        removeImageFromSquare(square);
    });
}

// Function to create images on the board based on the spot matrix
function createBoardImages(spot_matrix) {
    for (const row_ of spot_matrix) {
        for (const element of row_) {
            var piece = element["piece_name"];
            var is_white = element["color"];
            var col = element["col"];
            var row = element["row"];
            var color;

            if (is_white) {
                color = "white";
            } else if (is_white === false) {
                color = "black";
            } else if (is_white === 'x') {
                color = 'x';
            }

            var square = getSquareByCoordinates(row, col);
            if (piece !== 'x') {
                createImageFromSquare(square, color, piece);
            }
        }
    }
}

// Function to update the chessboard periodically
function updateChessboard() {
    getBoardState(function(responseData) {
        var spot_matrix = responseData["spot_matrix"];
        clearBoardImages();
        createBoardImages(spot_matrix);
    });
}

// Function to create and reset the chessboard with the spot matrix
function createResetChessboard(spot_matrix) {
    for (const row_ of spot_matrix) {
        for (const element of row_) {
            var piece = element["piece_name"];
            var is_white = element["color"];
            var col = element["col"];
            var row = element["row"];
            var color;

            if (is_white) {
                color = "white";
            } else if (is_white === false) {
                color = "black";
            } else if (is_white === 'x') {
                color = 'x';
            }

            var square = document.createElement('div');
            square.className = 'square ' + (row % 2 === col % 2 ? 'white' : 'black');
            square.setAttribute('data-row', row);
            square.setAttribute('data-col', col);

            if (piece !== 'x') {
                createImageFromSquare(square, color, piece);
                console.log(`Creating ${piece} image at row ${row} and at col ${col}`);
            }

            square.addEventListener('click', handleSquareClick);
            chessboardContainer.appendChild(square);
        }
    }
}

// Function to handle the reset button click
function handleResetClick() {
    console.log('Reset button clicked');
    sendResetToBackend(function(responseData) {
        console.log('Handling reset response:', responseData);

        clearBoardGraphics();
        var spot_matrix = responseData["spot_matrix"];
        createResetChessboard(spot_matrix);
    });
}

// Function to handle square click for making moves
function handleSquareClick(event) {
    var clickedSquare = event.currentTarget;
    var col = clickedSquare.getAttribute('data-col');
    var row = clickedSquare.getAttribute('data-row');

    if (firstClick === null) {
        // First click
        firstClick = { row: row, col: col };
        clickedSquare.classList.add('clicked'); // Add a class for clicked style
        console.log('First click:', firstClick);
    } else {
        // Second click
        var secondClick = { row: row, col: col };
        console.log('Second click:', secondClick);

        sendMovesToBackend(firstClick, secondClick, function(responseData) {
            console.log(responseData);

            let status = responseData["status"];
            if (status === 'Invalid move'){
                getSquareByCoordinates(firstClick.row, firstClick.col).classList.remove('clicked');
                firstClick = secondClick;
                getSquareByCoordinates(secondClick.row, secondClick.col).classList.add('clicked');
                secondClick = null;
            }else {
                var sqToRem = getSquareByCoordinates(firstClick.row, firstClick.col);
                var piece = responseData["piece"];
                var color = responseData["color"];

                if (piece !== 'x') {
                    removeImageFromSquare(sqToRem);
                    console.log(color);
                    console.log(piece);

                    var color2 = (color === 'white') ? 'black' : 'white';
                    var heading = document.getElementById('turn');
                    heading.textContent = "It is " + color2 + "'s turn";

                    var sq = getSquareByCoordinates(secondClick.row, secondClick.col);
                    removeImageFromSquare(sq);
                    createImageFromSquare(sq, color, piece);
                }

                var piece_2 = responseData["piece_2"];
                console.log('Piece_2:', piece_2);
                if (piece_2 === "rook") {
                    var sq_2_to_remove = getSquareByCoordinates(responseData["row"], responseData["img_col"]);
                    console.log(sq_2_to_remove);
                    removeImageFromSquare(sq_2_to_remove);

                    var sq_2_to_img = getSquareByCoordinates(responseData["row"], responseData["col"]);
                    console.log(sq_2_to_img);

                    createImageFromSquare(sq_2_to_img, color, "rook");
                    piece_2 = null;
                }

                console.log('Response from server:', responseData);

                getSquareByCoordinates(firstClick.row, firstClick.col).classList.remove('clicked');
                getSquareByCoordinates(secondClick.row, secondClick.col).classList.remove('clicked');                firstClick = null;
                firstClick = null;
                secondClick = null;

                if (status === 'win') {
                    let heading = document.getElementById('turn');
                    heading.textContent = "Game Over";
                    for (square of document.querySelectorAll('.square')) {
                        square.removeEventListener('click', handleSquareClick);
                    }
                    console.log('Game Over');
                }
            }
            console.log('First click after response:', firstClick);
            console.log('Second click after response:', secondClick);
        });
    }
}

// Function to fetch the board state from the server
function getBoardState(onResponse) {
    fetch('/api', { method: 'GET' })
    .then(response => response.json())
    .then(data => { onResponse(data); })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to send reset request to the server
function sendResetToBackend(onResponse) {
    fetch('/reset', { method: 'GET' })
    .then(response => response.json())
    .then(data => { onResponse(data); })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to send move data to the server
function sendMovesToBackend(firstClick, secondClick, onResponse) {
    fetch('/make_moves', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json;charset=UTF-8' },
        body: JSON.stringify({ firstClick: firstClick, secondClick: secondClick })
    })
    .then(response => response.json())
    .then(data => { onResponse(data); })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to remove image from a square
function removeImageFromSquare(square) {
    var image = square.querySelector('.chess-piece');
    if (image) {
        square.removeChild(image);
    }
}

// Function to get a square by its coordinates
function getSquareByCoordinates(row, col) {
    var selector = `[data-row='${row}'][data-col='${col}']`;
    return document.querySelector(selector);
}

// Function to create an image on a square
function createImageFromSquare(square, color, piece) {
    var image = document.createElement('img');
    image.src = `/static/chess/${color}_${piece}.png`;
    image.className = 'chess-piece';
    image.alt = `${color} ${piece}`;
    square.appendChild(image);
}
