var selectors = [];

var modules = [[["How to use ChessEDU", "1"], ["Pieces of the Game", "2"], ["Basic Movement", "3"], ["Your First Game", "4"], ["Avoiding an Early Defeat", "5"]],
                [["Defending", "6"], ["Castling", "7"], ["Pins and Skewers", "8"], ["Forcing Moves", "9"], ["Discovered Moves", "10"], ["The Ladder Checkmate", "11"]]];

function fillSelectors() {
  document.querySelectorAll('.module-container').forEach(item => {
    selectors.push(0);
  })
  console.log(selectors)
}

function updateLessons(boxes, moduleIndex) {
  for (let i = 0; i < boxes.length; i++) {
    boxes[i].childNodes[1].textContent = modules[moduleIndex][(selectors[moduleIndex] + i )% modules[moduleIndex].length][0];
    boxes[i].setAttribute("onclick", "window.location.href='/course/lesson" + modules[moduleIndex][(selectors[moduleIndex] + i )% modules[moduleIndex].length][1] + "'");
    console.log(boxes[i].onclick);
  }
}

function next(index) {
  if (selectors.length == 0) {
    fillSelectors();
  }
  selectors[index]++;
  var rightArrows = document.getElementsByClassName('right-arrow');
  var lessonBoxes = rightArrows[index].parentElement.getElementsByClassName('lesson-box');
  console.log(selectors)
  updateLessons(lessonBoxes, index);
}

function previous(index) {
  if (selectors.length == 0) {
    fillSelectors();
  }
  if (selectors[index] > 0) {
    selectors[index]--;
  }
  var leftArrows = document.getElementsByClassName('left-arrow');
  var lessonBoxes = leftArrows[index].parentElement.getElementsByClassName('lesson-box');
  updateLessons(lessonBoxes, index);
}
