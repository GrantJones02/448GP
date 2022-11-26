console.log("heck");

let leftarrow = document.getElementById('basic_left');
let rightarrow = document.getElementById('basic_right');
let box1 = document.getElementById('box1');
let box2 = document.getElementById('box2');
let box3 = document.getElementById('box3');
let selector = 0;

// Maybe change this into a list of objects that contain the className and then a link? Hmm..
let basic_lessons = [
    "piece button pawn",
    "piece button knight",
    "piece button bishop",
    "piece button rook",
    "piece button queen",
    "piece button king",
];

leftarrow.addEventListener('click', (e) => {
    selector--;
    updateBasicLessons();
})

rightarrow.addEventListener('click', (e) => {
    selector++;
    updateBasicLessons();
})

function updateBasicLessons() {
    box1.className = basic_lessons[selector % 5];
    box2.className = basic_lessons[(selector + 1) % 5];
    box3.className = basic_lessons[(selector + 2) % 5];
}

let basic_lesson_buttons = [box1, box2, box3];
for (let i = 0; i < basic_lesson_buttons.length; i++) {
    basic_lesson_buttons[i].addEventListener('click', (e) => {
        // Re-code so that it redirects to correct HTML page, maybe with switch statement?
        alert(basic_lesson_buttons[i].className);
    })
}

updateBasicLessons();
