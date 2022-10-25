var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
const rows = 8;
const columns = 8;
var cellSize = 60;
var colorOne = "DarkOliveGreen";
var colorTwo = "DarkKhaki"
var highlightedSquare;
var selected = 0;

var initialRow = '1';
var initialColumn = '2';
var pieceOfChoice = 'BQ';

// This variable will be used to hold each squre's piece!
var boardElements = [];
// Can be empty string ("") or a two-character string representing the color and then the piece
// i.e. BR = Black Rook, WR = White Rook, WP = White Pawn, etc
// IMPORTANT NOTE: Knights are abbreivated to N, so Black Knight is BN

var moveSelect = [];

function createBoardElements(array) {
    for (let i = 0; i < rows; i++) {
        let tempArray = [];
        for (let j = 0; j < columns; j++) {
            tempArray.push("");
        }
        array.push(tempArray);
    }

    console.log(array);
}

function drawBoard() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    selected = 0;
    let x, y;

    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < columns; j++) {
            let color = i;
            j % 2 ? color++ : color = color;
            color % 2 ? ctx.fillStyle = colorOne : ctx.fillStyle = colorTwo;
            if ((i.toString() + j.toString()) == highlightedSquare) {
                (color % 2) ? ctx.fillStyle = "Olive" : ctx.fillStyle = "Khaki";
                if (boardElements[i][j] != "") {
                    selected = 1;
                    x = i;
                    y = j;
                }
            };
            ctx.fillRect(cellSize * j, cellSize * i, cellSize, cellSize);
        }
    }

    if (selected) {
        drawValidMoves(x, y);
    }

    displayPieces();
}

function displayPieces() {
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < columns; j++) {
            let pieceToDraw = "";

            switch (boardElements[i][j]) {
                case 'BR':
                    pieceToDraw = "static/pieces/rook_b.png";
                    break;
                case 'WN':
                    pieceToDraw = "static/pieces/rook_w.png";
                    break;
                case 'WN':
                    pieceToDraw = "static/pieces/knight_w.png";
                    break;
                case 'BN':
                    pieceToDraw = "static/pieces/knight_b.png";
                    break;
                case 'BK':
                    pieceToDraw = "static/pieces/king_b.png";
                    break;
                case 'WK':
                    pieceToDraw = "static/pieces/king_w.png";
                    break;
                case 'WP':
                    pieceToDraw = "static/pieces/pawn_w.png";
                    break;
                case 'BP':
                    pieceToDraw = "static/pieces/pawn_b.png";
                    break;
                case 'WB':
                    pieceToDraw = "static/pieces/bishop_w.png";
                    break;
                case 'BB':
                    pieceToDraw = "static/pieces/bishop_b.png";
                    break;
                case 'WQ':
                    pieceToDraw = "static/pieces/queen_w.png";
                    break;
                case 'BQ':
                    pieceToDraw = "static/pieces/queen_b.png";
                    break;
            }

            if (pieceToDraw != "") {
                drawing = new Image();
                drawing.src = pieceToDraw;
                drawing.onload = function() {
                    ctx.drawImage(drawing,j*cellSize,i*cellSize);
                };
            }
        }
    }
}

function createButtons() {
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < columns; j++) {
            let button = document.createElement("button");
            button.id = "button" + i + j;
            button.classname = "boardButton " + i + j;
            button.style.position = "absolute";
            button.style.height = cellSize + "px";
            button.style.width = cellSize + "px";
            button.style.left = (cellSize * j + 8) + "px";
            button.style.top = (cellSize * i + 8) + "px";
            button.style.opacity = 0 + "%";
            button.onclick = function(e) {
                console.log(i.toString() + j.toString());
                let previousSelect = highlightedSquare;
                highlightedSquare = i.toString() + j.toString();
                if (selected) { // Need to add valid check for valid move
                    movePiece(previousSelect, highlightedSquare);
                }
                drawBoard();
            }
            document.body.appendChild(button);
        }
    }
}

function drawValidMoves() {
    let temp = ctx.fillStyle;
    ctx.fillStyle = "white";
    // I think I am going to have to switch to recursion

            for (let i = 0; i < rows; i++) {
                for (let j = 0; j < columns; j++) {
                    if (validMoves[i][j] == "1") {
                        //ctx.beginPath();
                        //ctx.arc(getPos(j), getPos(i), 8, 0, 2 * Math.PI);
                        //ctx.fill();
                        drawMoveCircle(j, i);
                    }
                }
            }

}

function drawMoveCircle(x, y) {
    ctx.fillStyle = "white";
    ctx.beginPath();
    ctx.arc(cellSize * (x + 0.5), cellSize * (y + 0.5), 8, 0, 2 * Math.PI);
    ctx.fill();
}

// probably should be moved to a new file
function movePiece(old_pos, new_pos) {

    console.log("old: " + old_pos[0] + ", " + old_pos[1]);
    console.log("new: " + new_pos[0] + ", " + new_pos[1]);

    let temp = boardElements[old_pos[0]][old_pos[1]];
    if(isValidMove(new_pos[0], new_pos[1]))
    {
        console.log("This is a valid move for this piece!");
        boardElements[old_pos[0]][old_pos[1]] = "";
        boardElements[new_pos[0]][new_pos[1]] = temp;
        viewNewValidMoves(new_pos[0], new_pos[1]);
    }
}

function main() {
    createBoardElements(boardElements);
    createBoardElements(moveSelect);
    boardElements[initialRow][initialColumn] = pieceOfChoice;
    drawBoard();
    createButtons();


    /* Basic template to draw pieces on board, using this for displayPieces() function!
    drawing = new Image();
    drawing.src = "pieces/bishop_b.png";
    drawing.onload = function() {
        ctx.drawImage(drawing,0,0);
    };
    */
}

main();
