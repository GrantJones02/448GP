// Objective:
// I'm about to make a BUNCH of event handlers
// and we'll see where it goes from there

function initialize()
{
    makeChessSquaresClickable();
}

function scream(dataSquare)
{
    console.log(dataSquare);
}

function makeChessSquaresClickable()
{
    let squares = document.getElementsByClassName("square-55d63");
    for(let i = 0; i < 64; i++)
    {
        let dataSquare = squares[i].getAttribute("data-square");
        squares[i].onclick = function(){scream(dataSquare)};
    }
}