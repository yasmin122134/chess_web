




document.addEventListener("DOMContentLoaded", function() {

    // Initialize the chessboard
    createChessboard();
});

var firstClick = null;
var chessboardContainer = document.getElementById('chessboard-container');
var resetButton = document.getElementById('reset-button');
resetButton.addEventListener('click', handleResetClick);

function createChessboard() {

    getBoardState(function(responseData){

    var spot_matrix = responseData["spot_matrix"];
       createResetChessboard(spot_matrix);
//        var resetButton = document.getElementById('reset-button');
//        resetButton.addEventListener('click', handleResetClick);
    });

}
function clearBoardGraphics() {
    var chessboardContainer = document.getElementById('chessboard-container');
    chessboardContainer.innerHTML = '';  // Clear the entire content of the container
}

function createResetChessboard(spot_matrix){

for (const row_ of spot_matrix) {
    for (const element of row_) {
    console.log(element)
        var piece = element["piece_name"];
        var is_white = element["color"];
        var col = element["col"];
//                console.log("the col is ${col}")
        var row = element["row"] ;
//                console.log("the row is ${row}")

        var color;
        if (is_white){
            color = "white";
        }

        if(is_white == false){
            color = "black";
        }

        if (is_white == 'x'){
            color = 'x';
        }


        var square = document.createElement('div');
        square.className = 'square ' + (row % 2 === col % 2 ? 'white' : 'black');
        square.setAttribute('data-row', row);
        square.setAttribute('data-col', col);


        if (piece != 'x'){
            createImageFromSquare(square, color, piece)
            console.log(`creating ${piece} image at row ${row} and at col ${col}`);
        }

        square.addEventListener('click', handleSquareClick);
        chessboardContainer.appendChild(square);
        }
    }

}

function handleResetClick(event){
    console.log('Reset button clicked');
    sendResetToBackend(function (responseData){
    console.log('Handling reset response:', responseData);

    clearBoardGraphics();

    var spot_matrix = responseData["spot_matrix"];
    createResetChessboard(spot_matrix)
    });
}

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

        sendMovesToBackend(firstClick, secondClick,
        function(responseData){

        // Handle the response data here
        console.log(responseData)
        sqToRem = getSquareByCoordinates(firstClick.row, firstClick.col)

        var piece = responseData["piece"];
        if (piece != 'x'){
            removeImageFromSquare(sqToRem)
            var color = responseData["color"];
            console.log(color)
            console.log(piece)

            var sq = getSquareByCoordinates(secondClick.row, secondClick.col)
            removeImageFromSquare(sq);
            createImageFromSquare(sq, color, piece);
        }

        var piece_2 = responseData["piece_2"];
        console.log('Piece_2:', piece_2);
        if (piece_2 == "rook"){
//            var sq_2_to_remove = getSquareByCoordinates(parseInt(responseData["row"]),(parseInt(responseData["col"])/3)*7)

            var sq_2_to_remove = getSquareByCoordinates(responseData["row"], responseData["img_col"])
            console.log(sq_2_to_remove)
            removeImageFromSquare(sq_2_to_remove)

//            var sq_2_to_img = getSquareByCoordinates(parseInt(responseData["row"]), parseInt(responseData["col"]));
            var sq_2_to_img = getSquareByCoordinates(responseData["row"], responseData["col"]);

            console.log(sq_2_to_img)
            var color = responseData["color"];


            createImageFromSquare(sq_2_to_img, color, "rook")
            piece_2 = null;
        }






        console.log('Response from server:', responseData);

        // Reset for the next pair of clicks
        firstClick = null;

        // Remove the clicked class to reset the style
        var allSquares = document.querySelectorAll('.square');
        allSquares.forEach(square => {
            square.classList.remove('clicked');
        });
    });



    }
}

function getBoardState(onResponse){
    fetch('/api',{method: 'GET',})
    .then(response => response.json())
    .then(
    data => {onResponse(data);}
    )
    .catch(error => {
        console.error('Error:', error);
    });

}

function sendResetToBackend(onResponse){
    fetch('/reset', {method: 'GET',})
    .then(response => response.json())
    .then(data => {onResponse(data);})
    .catch(error => {
        console.error('Error:', error);
    });
}


function sendMovesToBackend(firstClick, secondClick, onResponse) {
    fetch('/make_moves', {method: 'POST', headers: {'Content-Type': 'application/json;charset=UTF-8',},
     body: JSON.stringify({firstClick: firstClick, secondClick: secondClick,}),})
    .then(response => response.json())
    .then(data => {onResponse(data);})
    .catch(error => {
        console.error('Error:', error);
    });
}


function removeImageFromSquare(square) {
    // Check if the square contains an image
    var image = square.querySelector('.chess-piece');
    if (image) {
        // Remove the image from the square
        square.removeChild(image);
    }
}


function getSquareByCoordinates(row, col) {
    var selector = `[data-row='${row}'][data-col='${col}']`;
    return document.querySelector(selector);
}

function createImageFromSquare(square, color, piece){
    var image = document.createElement('img');
    image.src = `/static/chess/${color}_${piece}.png`;
    image.className = 'chess-piece';
    image.alt = "${color} ${piece}";
    square.appendChild(image);
}








