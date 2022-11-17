// Objective:
// I'm about to make a BUNCH of event handlers
// and we'll see where it goes from there

var outcomeToDisplay = "waiting";

function initialize()
{
    makeChessSquaresClickable();
}

function scream(dataSquare)
{
    console.log(dataSquare);
}

function showAllFeedback()
{
    showTextFeedback();
    showPieceMove();
}

function showTextFeedback()
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

function showPieceMove()
{

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