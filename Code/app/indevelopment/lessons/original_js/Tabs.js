class Tabs {
    constructor(source) {
        this.visibleSection = 0;
        this.path = document.getElementById(source);
        this.size = document.getElementById(source).children.length;
        hide(this);
    }
}
  
function hide(tab)
{
    for(let i = 0; i < tab.size; i++)
    {
        if(i == tab.visibleSection)
        {
            tab.path.children[i].style.display = "";        // make not hidden
        }
        else    // if section should not be visible
        {
            tab.path.children[i].style.display = "none";    // make hidden, don't make space for this
        }
    }
}
  
function previous(tab)
{
    if(tab.visibleSection == 0)
    {
        tab.visibleSection = tab.size - 1;
    }
    else
    {
        tab.visibleSection -= 1;
    }
    hide(tab);
}
  
function next(tab)
{
    if(tab.visibleSection == tab.size - 1)
    {
        tab.visibleSection = 0;
    }
    else
    {
        tab.visibleSection += 1;
    }
    hide(tab);
}