let socket = io.connect('http://' + document.domain + ':' + location.port);
let firstClick = null;
let secondClick = null;

document.addEventListener("DOMContentLoaded", function() {
    socket.emit('connecting');
    // initializeChessboard();
});


socket.on('update_board', function(data) {
    console.log('update_board event received');
    console.log(data.status);
    if (data.status !== 'Invalid move') {
        var spot_matrix = data.spot_matrix;
        clearBoardImages();
        createBoardImages(spot_matrix);
        removeClickedClassFromAllSquares();
        var heading = document.getElementById('turn');
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

socket.on('update_massage', function(data) {
    var heading = document.getElementById('funny');
    console.log(data)
    heading.textContent = data;
});
socket.on('init_board', function(data) {
    var spot_matrix = data.spot_matrix;
    createChessboard(spot_matrix);
    console.log(spot_matrix);
    // clearBoardImages();
    // createBoardImages(spot_matrix);

});


const chessboardContainer = document.getElementById('chessboard-container');
const resetButton = document.getElementById('reset-button');
resetButton.addEventListener('click', handleResetClick);

function getBoardState() {
    socket.emit('get_board_state');

}

function clearBoardGraphics() {
    chessboardContainer.innerHTML = '';
}

function clearBoardImages() {
    var allSquares = document.querySelectorAll('.square');
    allSquares.forEach(square => {
        removeImageFromSquare(square);
    });
}

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

function handleResetClick() {
    socket.emit('reset_game');
}

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
        socket.emit('make_moves', { firstClick: firstClick, secondClick: secondClick});
        console.log('Sent make_move event');
        firstClick = null;
        removeClickedClassFromAllSquares();
    }
}

function removeClickedClassFromAllSquares() {
    var allSquares = document.querySelectorAll('.square');
    allSquares.forEach(square => {
        square.classList.remove('clicked');
    });
}

function getSquareByCoordinates(row, col) {
    var selector = `[data-row='${row}'][data-col='${col}']`;
    return document.querySelector(selector);
}

function createImageFromSquare(square, color, piece) {
    var image = document.createElement('img');
    image.src = `/static/chess/${color}_${piece}.png`;
    image.className = 'chess-piece';
    image.alt = `${color} ${piece}`;
    square.appendChild(image);
}

function removeImageFromSquare(square) {
    var image = square.querySelector('.chess-piece');
    if (image) {
        square.removeChild(image);
    }
}

// Initialize the chessboard and add event listeners to squares
function initializeChessboard() {
    // socket.emit('get_board_state');
    createChessboard();
    // getBoardState();
    document.querySelectorAll('.square').forEach(square => {
        square.addEventListener('click', handleSquareClick);
    });
}

// // Listen for initial board state
// socket.on('board_state', function(responseData) {
//     var spot_matrix = responseData.spot_matrix;
//     console.log(spot_matrix);
//     clearBoardGraphics();
//     createResetChessboard(spot_matrix);
// });

// Function to create and reset the chessboard with the spot matrix
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
