// Given a coordinate and a piece
// Find valid moves for that piece

// Recursively: Rook, Bishop, Queen
// Basic: Knight, Pawn, King

//0: Global Variables and Initialization Tools

// arrayToUpdate is a global flag needed for the King behavior.
// this string tells the mark() function which array to mark on.
// it is under most circumstances set to "validMoves",
// but during the king move calculation we need to validate positions
// that are safe for the king to move to.
// during this time, we change the flag and change it back afterward.

var validMoves = [];
for (let i = 0; i < 8; i++) {
    let tempArray = [];
    for (let j = 0; j < 8; j++) {
        tempArray.push("0");
    }
    validMoves.push(tempArray);
}
initializeValidMoves();

function initializeValidMoves(){
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            validMoves[i][j] = "0";
            console.log(validMoves[i][j]);
        }
    }
}

var takenSpaces = [];
takenSpaces = [];
for(let i = 0; i < 8; i++) {
    let tempArray2 = [];
    for (let j = 0; j < 8; j++) {
        // what pieces are where?
        if(boardElements[i][j] != ""){ // there is a piece here!
            tempArray2.push("1");
        }
        else{ // there is not a piece here!
            tempArray2.push("0");
        }
    }
    takenSpaces.push(tempArray2);
}
initializeTakenSpaces();

function initializeTakenSpaces(){
    for(let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            // what pieces are where?
            if(boardElements[i][j] != ""){ // there is a piece here!
                takenSpaces[i][j] = "1";
            }
            else{ // there is not a piece here!
                takenSpaces[i][j] = "0";
            }
        }
    }
}

//1: Valid Moves Functions
function showValidMoves(row, column) {
    // notifying the console the function is running,
    // and that it has the correct coordinates
    console.log("I am testing the move!");
    console.log(row);
    console.log(column);

    row = parseInt(row);
    column = parseInt(column);

    // finding the piece for the position we want to move to
    let piece = boardElements[row][column];

    // sending the correct piece to console
    console.log("The piece we are moving should be:\n");
    console.log(piece);
    // finding the correct path
    if(piece == "WP" || piece == "BP"){
        if(piece == "WP"){
            showValidPawnMoves(row, column, "white");
        }
        else{
            showValidPawnMoves(row, column, "black")
        }
    }
    else if(piece == "WR" || piece == "BR"){
        console.log("I'm going to the rook moves section!");
        showValidRookMoves(row, column, findColor(piece))
    }
    else if(piece == "WN" || piece == "BN"){
        showValidKnightMoves(row, column, findColor(piece))
    }
    else if(piece == "WB" || piece == "BB"){
        showValidBishopMoves(row, column, findColor(piece))
    }
    else if(piece == "WQ" || piece == "BQ"){
        showValidQueenMoves(row, column, findColor(piece))
    }
    else if(piece == "WK" || piece == "BK"){
        showValidKingMoves(row, column, findColor(piece))
    }
    return validMoves;
}

//1.0: General Tools
function isOccupied(row, column) {
    return(takenSpaces[row][column] == ("1"));
}
function mark(row, column) {
    console.log(`marking ${row} ${column}`)
    validMoves[row][column] = "1";
}
function outOfBounds(row, column) {
    if(row > 7 || row < 0){
        return(true)
    }
    if(column > 7 || column < 0){
        return(true)
    }
    return(false)
}
function findColor(piece)
{
    if (piece[0] == "W"){
        return("white");
    }
    if (piece[0] == "B"){
        return("black");
    }
    return("unknown");
}

//1.1: Pawn Logic
// the logic of the pawn depends on two things the four next pieces do not:
// - the color of the pawn, for direction
// - whether certain spaces are occupied (capturing, blocking in front, en passant)
// this actually makes its logic probably the most complex of any piece other than the king.
function showValidPawnMoves(row, column, color)
{
    row = parseInt(row);
    column = parseInt(column);

    let yDirection = 0;
    if(color = "white"){
        yDirection = -1;    // white starts at the bottom and moves up (negative)
    }
    else if(color = "black"){
        yDirection = 1;     // black starts at the top and moves down (positive)
    }

    // can I walk forward?
    let checkedRow = row + parseInt(yDirection);
    if( !(isOccupied(parseInt(checkedRow), column)) ){
        mark(checkedRow, column);
        // can I walk forward twice?
        if( !(isOccupied(checkedRow + yDirection, column)) ){
            if(color == "white" && row == 6){                   // these are the starting rows
                mark(checkedRow + yDirection, column);          // for black and white pawns
            }                                                   // respectively, and
            if(color == "black" && row == 1){                   // the pawns moving from here
                mark(checkedRow + yDirection, column);          // means they can no longer
            }                                                   // make a two-space move
        }
    }

    // can I capture diagonal?
    if( isOccupied(checkedRow, column - 1) ){
        mark(checkedRow, column - 1);
    }
    if( isOccupied(checkedRow, column + 1) ){
        mark(checkedRow, column + 1);
    }

    // finally, did an "en passant" move happen near me?
    // for the prototype: EN PASSANT IS DISABLED
    if(canEnPassant()){
        // the helper will pass the position we can capture to,
        // so diagonal left or diagonal right in the direction of the pawn's motion
        if( (enPassantPosition(yDirection) == [checkedRow, column + 1]) || (enPassantPosition(yDirection) == [checkedRow, column + 1]) ){
            mark(enPassantPosition());
        }
    }
}

// this helper is a boolean function!
// it returns whether the last move to occur would allow for an "en passant"
// the next turn.
// this will check the list of moves to see if the last move was:
// "other color" moved pawn two spaces
// the only move that can precede en passant.
function canEnPassant()
{
    // temp fix...
    return false;
}

// this helper returns a list of 2 int coordinates:
// the position that the pawn that just moved two spaces could be attacked against.
// this is the position the opponents pawn would be in, if only one space had been moved.
// we can find this space by finding the position the opposing pawn moved to,
// and adding the direction value of the moving pawn,
// since the white and black directions are reversed.
function enPassantPosition(direction)
{
    let moveDescription = ""; // replace with lookupLastMove()
    // process the string to get the position value
    let pawnPosition = [-99,-99]; // TEMPORARY GARBAGE VALUE! replace with actual string processing
    return(pawnPosition + direction);
}

//1.2: Rook Logic
function showValidRookMoves(row, column, color)
{
    console.log("I'm in the rook moves function!");
    //goal: divide case into recursion in each direction
    directionalLogicHelper(row, column, color, [-1, 0]);
    directionalLogicHelper(row, column, color, [1, 0]);
    directionalLogicHelper(row, column, color, [0, -1]);
    directionalLogicHelper(row, column, color, [0, 1]);
}

function directionalLogicHelper(row, column, color, progressor)
{
    // so how this works is:
    // the master function hands essentially a vector direction to the recursion.
    // we add this to the position each recursion to get to a new position.
    // if this position is out of bounds, we stop recursing without marking.
    // if this position is occupied: we mark this space and stop recursing (since this is a rook).
    // otherwise, we mark and continue recursion again.

    console.log("I'm doing recursion!");
    console.log(progressor);
    row = row + progressor[0];
    column = column + progressor[1];

    if(outOfBounds(row, column)){
        return;
    }
    if(isOccupied(row, column)){
        if(color != findColor(boardElements[row][column]))
        {
            mark(row, column);
        }
        return;
    }
    //otherwise
    mark(row, column);
    directionalLogicHelper(row, column, color, progressor);
}

//1.3: Knight Logic
// this method does not require recursion,
// but we need to figure out a way to represent the "L-shape" pattern it follows.
// we will create a list that includes all options to move two, then move one.
function showValidKnightMoves(row, column, color)
{
    let testrow = row;
    let testcolumn = column;
    let myLshapes = [ [2,1],[2,-1],[-2,1],[-2,-1],[1,2],[-1,2],[1,-2],[-1,-2] ];
    for(let i = 0; i < 8; i++){
        testrow = row + myLshapes[i][0];
        testcolumn = column + myLshapes[i][1];
        if( !( outOfBounds(testrow, testcolumn) ) ){
            if(color != findColor(boardElements[testrow][testcolumn]))
            {
                mark(testrow, testcolumn);
            }
        }
        testrow = row;
        testcolumn = column;
    }
}

//1.4: Bishop Logic
// this is the same idea as the rook, but we use diagonal progressors
function showValidBishopMoves(row, column, color)
{
    console.log("I'm in the bishop moves function!");
    //goal: divide case into recursion in each direction
    directionalLogicHelper(row, column, color, [-1, -1]);
    directionalLogicHelper(row, column, color, [-1, 1]);
    directionalLogicHelper(row, column, color, [1, -1]);
    directionalLogicHelper(row, column, color, [1, 1]);
}

//1.5: Queen Logic
// the queen has the same powers as the bishop and the rook combined,
// so we use essentially the same logic here of both combined
function showValidQueenMoves(row, column, color)
{
    console.log("I'm in the queen moves function!");
    //goal: divide case into recursion in each direction
    directionalLogicHelper(row, column, color, [-1, -1]);
    directionalLogicHelper(row, column, color, [-1, 1]);
    directionalLogicHelper(row, column, color, [1, -1]);
    directionalLogicHelper(row, column, color, [1, 1]);
    directionalLogicHelper(row, column, color, [-1, 0]);
    directionalLogicHelper(row, column, color, [1, 0]);
    directionalLogicHelper(row, column, color, [0, -1]);
    directionalLogicHelper(row, column, color, [0, 1]);
}

//1.6: King Logic
// the king is the only piece which has its movement limited by attacks from other pieces.
// its logic must be saved for last.
// NOTE: For the prototype, we are not handling checks.
// As a result, the king logic is going to be significantly reduced.
function showValidKingMoves(row, column, color)
{
    // note that since the king has an easy to list number of moves,
    // we can write this similar to the knight.
    // if we had check, we'd need a much more complex function.
    let testrow = row;
    let testcolumn = column;
    let maximumMoves = [ [0,1],[0,-1],[1,1],[1,0],[1,-1],[-1,1],[-1,0],[-1,-1] ]
    for(let i = 0; i < 8; i++){
        testrow = parseInt(row) + parseInt(maximumMoves[i][0]);
        testcolumn = parseInt(column) + parseInt(maximumMoves[i][1]);
        if( !( outOfBounds(testrow, testcolumn) ) ){
            console.log(color);
            console.log([testrow, testcolumn])
            console.log(boardElements[testrow][testcolumn]);
            console.log(boardElements);
            console.log(findColor(boardElements[testrow][testcolumn]));
            if(color != findColor(boardElements[testrow][testcolumn]))
            {
                mark(testrow, testcolumn);
            }
        }
        testrow = row;
        testcolumn = column;
    }
}

function checkBoard(board) {
    let state = "";

    return state;
}

//2. Actual Move Validation
// goal: receive a move from index.js,
// and check if it is valid.
// we need a boolean for this.
function isValidMove(newRow, newColumn)
{
    console.log([newRow, newColumn]);
    console.log(validMoves[newRow][newColumn]);
    return(validMoves[newRow][newColumn] == "1");
}

//3. Adjusting Move View To New Position
// goal: after a new move that is valid,
// we want to see the new moves available this turn.
function viewNewValidMoves(row, column)
{
    console.log("I got this far at least!");
    initializeValidMoves(); // we reset the validMoves array to all zeroes
    console.log("this is what validMoves looks like after it should be reset:");
    console.log(validMoves);
    showValidMoves(row, column); // we then find the valid moves at this position
    drawValidMoves(); //we then illustrate this
}


console.log("takenSpaces looks like:\n");
console.log(takenSpaces);
console.log("validMoves looks like:\n");
showValidMoves(initialRow, initialColumn);
console.log(validMoves);
drawValidMoves();
