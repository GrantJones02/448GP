class ClickableImage {
    constructor(source) {
        
        this.path = document.getElementById(source);
        this.size = document.getElementById(source).children.length;
        this.feedbackPath = document.getElementById(source).children[2];
        this.currentOutcome = 0;        
        this.outcomes = fetchOutcomes(source);
        // An array of the different outcomes in order, besides the waiting message.
        showOutcomes(this);
    }
}

function fetchOutcomes(source)
{
    console.log("did it!\n");
    let outcomes = [];
    let path = document.getElementById(source);
    let feedbackPath = path.children[2];
    for(let i = 1; i < feedbackPath.children.length; i++)
    {
        console.log(feedbackPath.children[i].getAttribute("id"));
        outcomes[i-1] = feedbackPath.children[i].getAttribute("id");
    }
    console.log(outcomes);
    return outcomes;
} 

function showOutcomes(clickImg)
{
    for(let i = 0; i < clickImg.size; i++)
    {
        if(i == clickImg.currentOutcome)
        {
            clickImg.feedbackPath.children[i].style.display = "";        // make not hidden
        }
        else    // if section should not be visible
        {
            clickImg.feedbackPath.children[i].style.display = "none";    // make hidden, don't make space for this
        }
    }
}

function showFeedback(clickImg, passedOutcome)
{
    console.log(clickImg.outcomes);
    for(let i = 0; i < clickImg.outcomes.length; i++)
    {
        if(passedOutcome == clickImg.outcomes[i])
        {
            clickImg.currentOutcome = i+1;
            showOutcomes(clickImg);
        }
    }
}