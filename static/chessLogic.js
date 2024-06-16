// Establish connection with the server
let socket = io.connect('http://' + document.domain + ':' + location.port);
let firstClick = null;
let secondClick = null;

// Event listener for DOMContentLoaded event
document.addEventListener("DOMContentLoaded", function() {
    // Emit 'connecting' event when the DOM is fully loaded
    socket.emit('connecting');
});

// Event listener for 'update_board' event from the server
socket.on('update_board', function(data) {
    // Log the received data
    console.log('update_board event received');
    console.log(data.status);
    if (data.status !== 'Invalid move') {
        var spot_matrix = data.spot_matrix;
        // Clear the board and create new images
        clearBoardImages();
        createBoardImages(spot_matrix);
        removeClickedClassFromAllSquares();
        var heading = document.getElementById('turn');
        // Update the heading with the current turn
        heading.textContent = "It is " + data.turn + "'s turn";

        firstClick = null;
    } else {
        console.log('move was invalid');
        console.log('first click:', firstClick);
        console.log('second click:', secondClick);
        if (secondClick !== null) {
            removeClickedClassFromAllSquares();
            firstClick = secondClick;
            console.log('new First click:', firstClick);
            getSquareByCoordinates(secondClick.row, secondClick.col).classList.add('clicked');
        }
    }
});

// Event listener for 'update_massage' event from the server
socket.on('update_massage', function(data) {
    var heading = document.getElementById('funny');
    console.log(data)
    // Update the heading with the received data
    heading.textContent = data;
});

// Event listener for 'init_board' event from the server
socket.on('init_board', function(data) {
    var spot_matrix = data.spot_matrix;
    // Create the chessboard with the received spot matrix
    createChessboard(spot_matrix);
    console.log(spot_matrix);
});

// Get the chessboard container and reset button elements
const chessboardContainer = document.getElementById('chessboard-container');
const resetButton = document.getElementById('reset-button');
// Add event listener for click event on the reset button
resetButton.addEventListener('click', handleResetClick);

// Function to emit 'get_board_state' event to the server
function getBoardState() {
    socket.emit('get_board_state');
}

// Function to clear the chessboard graphics
function clearBoardGraphics() {
    chessboardContainer.innerHTML = '';
}

// Function to clear the images from the chessboard
function clearBoardImages() {
    var allSquares = document.querySelectorAll('.square');
    allSquares.forEach(square => {
        removeImageFromSquare(square);
    });
}

// Function to create images on the chessboard
function createBoardImages(spot_matrix) {
    for (const row_ of spot_matrix) {
        for (const element of row_) {
            var piece = element["piece_name"];
            var is_white = element["color"];
            var col = element["col"];
            var row = element["row"];
            var color = is_white ? "white" : (is_white === false ? "black" : 'x');

            var square = getSquareByCoordinates(row, col);
            if (piece !== 'x') {
                createImageFromSquare(square, color, piece);
            }
        }
    }
}

// Function to handle click event on the reset button
function handleResetClick() {
    // Emit 'reset_game' event to the server
    socket.emit('reset_game');
}

// Function to handle click event on a square
function handleSquareClick(event) {
    var clickedSquare = event.currentTarget;
    var col = clickedSquare.getAttribute('data-col');
    var row = clickedSquare.getAttribute('data-row');

    if (firstClick === null) {
        firstClick = { row: row, col: col };
        clickedSquare.classList.add('clicked');
        console.log('First click:', firstClick);
    } else {
        secondClick = { row: row, col: col };
        console.log('Second click:', secondClick);
        console.log('Sending make_move event');
        // Emit 'make_moves' event to the server
        socket.emit('make_moves', { firstClick: firstClick, secondClick: secondClick});
        console.log('Sent make_move event');
        firstClick = null;
        removeClickedClassFromAllSquares();
    }
}

// Function to remove 'clicked' class from all squares
function removeClickedClassFromAllSquares() {
    var allSquares = document.querySelectorAll('.square');
    allSquares.forEach(square => {
        square.classList.remove('clicked');
    });
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

// Function to remove an image from a square
function removeImageFromSquare(square) {
    var image = square.querySelector('.chess-piece');
    if (image) {
        square.removeChild(image);
    }
}

// Function to initialize the chessboard
function initializeChessboard() {
    createChessboard();
    document.querySelectorAll('.square').forEach(square => {
        square.addEventListener('click', handleSquareClick);
    });
}

// Function to create the chessboard
function createChessboard(spot_matrix) {
    for (const row_ of spot_matrix) {
        for (const element of row_) {
            var piece = element["piece_name"];
            var is_white = element["color"];
            var col = element["col"];
            var row = element["row"];
            var color = is_white ? "white" : (is_white === false ? "black" : 'x');

            var square = document.createElement('div');
            square.className = 'square ' + (row % 2 === col % 2 ? 'white' : 'black');
            square.setAttribute('data-row', row);
            square.setAttribute('data-col', col);

            if (piece !== 'x') {
                createImageFromSquare(square, color, piece);
            }

            square.addEventListener('click', handleSquareClick);
            chessboardContainer.appendChild(square);
        }
    }
}

// Initialize the chessboard on page load
initializeChessboard();