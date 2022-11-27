let moduleBoxes = document.querySelectorAll('.module-container')
let lessonBoxes = document.querySelectorAll('.lesson-box')
let selectors = [];

// Maybe change this into a list of objects that contain the className and then a link? Hmm..
let modules = [
    [["How to use ChessEDU", "1"], ["Pieces of the Game", "2"], ["Basic Movement", "3"], ["Your First Game", "4"], ["Avoiding an Early Defeat", "5"]],
    [["Defending", "6"], ["Castling", "7"], ["Pins and Skewers", "8"], ["Forcing Moves", "9"], ["Discovered Moves", "10"], ["The Ladder Checkmate", "11"]],
];
document.querySelectorAll('.module-container').forEach(item => {
  selectors.push(0);
})
document.querySelectorAll('.lesson-box').forEach(item => {
  item.addEventListener('click', event => {
    alert(event.target.innerHTML);
  })
})

function updateLessons(lessons, moduleIndex) {
    lessons[0].childNodes[1].textContent = modules[moduleIndex][selectors[moduleIndex] % modules[moduleIndex].length][0];
    lessons[0].onclick = "/course/lesson" + modules[moduleIndex][selectors[moduleIndex] % modules[moduleIndex].length][1];
    lessons[1].childNodes[1].textContent = modules[moduleIndex][(selectors[moduleIndex] + 1) % modules[moduleIndex].length][0];
    lessons[1].onclick = "/course/lesson" + modules[moduleIndex][selectors[moduleIndex] % modules[moduleIndex].length][1];
    lessons[2].childNodes[1].textContent = modules[moduleIndex][(selectors[moduleIndex] + 2) % modules[moduleIndex].length][0];
    lessons[2].onclick = "/course/lesson" + modules[moduleIndex][selectors[moduleIndex] % modules[moduleIndex].length][1];
}

document.querySelectorAll('.left-arrow').forEach(item => {
  item.addEventListener('click', function(event){
    console.log("activated left listener");
    let leftArrows = document.querySelectorAll('.left-arrow');
    let targetElement = event.target;
    let index = 0;
    for (let i = 0; i < leftArrows.length; i++) {
      if (leftArrows[i]===targetElement) {
        index = i;
      }
    }
    let lessonBoxes = targetElement.parentElement.querySelectorAll('.lesson-box');
    if (selectors[index] > 0) {
      selectors[index]--;
      updateLessons(lessonBoxes, index);
    }
  })
})

let rightArrows = document.getElementsByClassName('right-arrow')
console.log(rightArrows.length)
for (let j = 0; j < rightArrows.length; j++) {
  console.log(j)
  rightArrows[j].addEventListener('click', function(event){
    let rightArrows = document.getElementsByClassName('right-arrow');
    let targetElement = event.target;
    let index = 0;
    for (let i = 0; i < rightArrows.length; i++) {
      if (rightArrows[i]===targetElement) {
        index = i;
      }
    }
    let lessonBoxes = targetElement.parentElement.getElementsByClassName('lesson-box');
    selectors[index]++;
    updateLessons(lessonBoxes, index);
  })
}

// This code sits as an example to how the script is displaying the DOM after interacting with Flask
console.log(document.getElementsByClassName('right-arrow'))
