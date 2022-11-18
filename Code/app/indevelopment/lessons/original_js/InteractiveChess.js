// Objective:
// I'm about to make a BUNCH of event listeners
// and we'll see where it goes from there

// Update:
// It seems to be going well

class InteractiveChess {
    constructor(inputOutcomes, inputPieces, inputAllowPieceMovement, inputPieceToMove, inputChessBoardJS) {

// INITIAL ATTRIBUTES TO SET
this.outcomeBoard = [
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','','']  
];
this.outcomeBoard = initializeOutcomes(this.outcomeBoard, inputOutcomes)

this.piecesBoard = [
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','',''],
    ['','','','','','','','']   
];
this.piecesBoard = initializePieces(this.piecesBoard, inputPieces)

this.pieceToMove = inputPieceToMove;

this.allowPieceMovement = inputAllowPieceMovement;

this.chessBoardJS = inputChessBoardJS;

// INITIAL FUNCTIONS TO RUN
initializeUI(this);
showTextFeedback("waiting");
    }
}

////    ////    ////    ////    ////
//      CONSTRUCTOR HELPER FUNCTIONS
////    ////    ////    ////    ////

function initializeOutcomes(board, outcomes)
{
    // expected input "outcomes": a 2d list with structure
    // [ ["good_outcome", "a1", "a2", "a3"],
    //   ["bad_outcome", "ALL ELSE"] 
    // ]

    // Figuring out which outcomes are "ALL ELSE"
    let rowsToSkip = []
    for(let i = 0; i < outcomes.length; i++)
    {
        // If the last element of the row is the phrase "ALL ELSE",
        // we want to override the process to set all of the board
        // to this value FIRST.
        // This saves us needing to track which positions have been set.
        if( outcomes[i][(outcomes[i].length - 1)] == "ALL ELSE" )
        {
            for(let x = 0; x < 8; x++)
            {
                for(let y = 0; y < 8; y++)
                {
                    board[x][y] = outcomes[i][0];
                }
            }
            rowsToSkip.push(i);
        }
    }

    // Setting outcomes that have specific coordinate instructions
    let tempPosition = [];
    let tempRow = [];
    let tempCol = [];
    for(let i = 0; i < outcomes.length; i++)
    {
        if(!(rowsToSkip.includes(i)))
        {
            for(let j = 1; j < outcomes[i].length; j++)
            {
                tempPosition = toArrayFormat(outcomes[i][j]);
                tempRow = tempPosition[0];
                tempCol = tempPosition[1];
                board[tempRow][tempCol] = outcomes[i][0];
            }
        }
    }
    return board;
}

function initializePieces(board, pieces)
{
    // expected input "pieces": a 2d list with structure
    // [ ["a1", "wK"],
    //   ["a2", "wK"],
    //   ["a3", "wK"] 
    // ]

    let tempPosition = [];
    let tempRow = [];
    let tempCol = [];
    for(let i = 0; i < pieces.length; i++)
    {
        tempPosition = toArrayFormat(pieces[i][0]);
        tempRow = tempPosition[0];
        tempCol = tempPosition[1];
        board[tempRow][tempCol] = pieces[i][1];
    }
    return board;
}

function initializeUI(myInteractiveChess)
{
    makeChessSquaresClickable(myInteractiveChess);
}

function makeChessSquaresClickable(myInteractiveChess)
{
    //the CSS class all the squares have
    let squares = document.getElementsByClassName("square-55d63");
    for(let i = 0; i < 64; i++)
    {
        let dataSquare = squares[i].getAttribute("data-square");
        squares[i].onclick = function(){checkSquare(myInteractiveChess, dataSquare)};
    }
}

////    ////    ////    ////    ////
//      OTHER FUNCTIONS
////    ////    ////    ////    ////

function toArrayFormat(dataSquare)
{
    let row = 0;
    let col = 0;
    // example: a8

    row = 8 - dataSquare.at(1);
    // The row values in standard chess format
    // has been implemented in chessboard.js
    // from bottom to top ascending.
    // to get in a format friendly for a list,
    // we subtract the number from 8.
    // Note: our array is zero-indexed!


    // The col value is in the correct order.
    switch(dataSquare.at(0)){
        case 'a':
            col = 0;
            break;
        case 'b':
            col = 1;
            break;
        case 'c':
            col = 2;
            break;
        case 'd':
            col = 3;
            break;
        case 'e':
            col = 4;
            break;
        case 'f':
            col = 5;
            break;
        case 'g':
            col = 6;
            break;
        case 'h':
            col = 7;
            break;
    }
    return([row, col]);
}

function toChessFormat(row, col)
{
    let rank = 8 - row;
    let file = "";
    switch(col){
        case 0:
            file = 'a';
            break;
        case 1:
            file = 'b';
            break;
        case 2:
            file = 'c';
            break;
        case 3:
            file = 'd';
            break;
        case 4:
            file = 'e';
            break;
        case 5:
            file = 'f';
            break;
        case 6:
            file = 'g';
            break;
        case 7:
            file = 'h';
            break;
    }
    return(file + rank);
}

function checkSquare(myInteractiveChess, dataSquare)
{
    let coords = toArrayFormat(dataSquare);
    let row = coords[0];
    let col = coords[1];
    
    outcomeToDisplay = myInteractiveChess.outcomeBoard[row][col];
    showTextFeedback(outcomeToDisplay);
    showPieceMove(myInteractiveChess, dataSquare);
}

function showTextFeedback(outcomeToDisplay)
{
    let outcomes = document.getElementById("feedback");
    for(let i = 0; i < outcomes.children.length; i++)
    {
        if(outcomes.children[i].id == outcomeToDisplay)
        {
            outcomes.children[i].style.display = "";        // make not hidden
        }
        else    // if section should not be visible
        {
            outcomes.children[i].style.display = "none";    // make hidden, don't make space for this
        }
    }
}

function showPieceMove(myInteractiveChess, dataSquare)
{
    let currentPosition = '';
    let coords = toArrayFormat(dataSquare);
    let row = coords[0];
    let col = coords[1];
    if(myInteractiveChess.allowPieceMovement)
    {
        for(let i = 0; i < 8; i++)
        {
            for(let j = 0; j < 8; j++)
            {
                if(myInteractiveChess.piecesBoard[i][j] == myInteractiveChess.pieceToMove)
                {
                    myInteractiveChess.piecesBoard[i][j] = '';  
                    currentPosition = toChessFormat(i,j);                 
                }
            }
        }
        myInteractiveChess.piecesBoard[row][col] = myInteractiveChess.pieceToMove;
        let moveFEN = currentPosition + "-" + dataSquare;
        myInteractiveChess.chessBoardJS.move(moveFEN);
    }
}