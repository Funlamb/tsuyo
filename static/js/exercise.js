var dateTimeName = "nDatetime[]"
var exerciseName = "nExercise[]"
var setNumberName = "nSetnumber[]"
var repName = "nRep[]"
var resistanceName = "nResistance[]"

let tabIndexNum = 1;
let datetime = $("#datetime");
let exercise = $("#exercise");
let setNumber = $("#setnumber");
let rep = $("#rep");
let resistance = $("#resistance");

function addRow(){
    //Date and Time
    var input = document.createElement("input");
    input.setAttribute("type", "datetime-local");
    input.setAttribute("name", dateTimeName);
    input.setAttribute("tabindex", tabIndexNum)
    input.setAttribute("autocomplete", "off");
    if (document.getElementById("datetime").firstChild){
        let datetimeValue = document.getElementById("datetime").lastElementChild.value;
        input.setAttribute("value", datetimeValue);
    } 
    var br = $("<br>");
    datetime.append(br);
    datetime.append(input);
    tabIndexNum++;
    
    //Exercise Input
    var inputDrop = document.createElement("input");
    inputDrop.setAttribute("name", exerciseName);
    inputDrop.setAttribute("tabindex", tabIndexNum);
    inputDrop.setAttribute("special", true);
    if(document.getElementById("exercise").firstChild){
        let exerciseValue = document.getElementById("exercise").lastElementChild.value;
        inputDrop.setAttribute("value", exerciseValue);
    }
    var br = $("<br>");
    exercise.append(br);
    exercise.append(inputDrop);
    tabIndexNum++;
    inputDrop.focus();

    //Set Number Inpute
    var input = document.createElement("input");
    input.setAttribute("type", "number");
    input.setAttribute("name", setNumberName);
    input.setAttribute("tabindex", tabIndexNum);
    input.setAttribute("autocomplete", "off");
    if(document.getElementById("setnumber").firstChild){
        let setNumberValue = parseInt(document.getElementById("setnumber").lastElementChild.value) + 1;
        input.setAttribute("value", setNumberValue);
    }
    var br = $("<br>");
    setNumber.append(br);
    setNumber.append(input);
    tabIndexNum++;
    
    //Repetition Input
    var input = document.createElement("input");
    input.setAttribute("type", "number");
    input.setAttribute("name", repName);
    input.setAttribute("tabindex", tabIndexNum);
    input.setAttribute("autocomplete", "off");
    if(document.getElementById("rep").firstChild){
        let repValue = parseInt(document.getElementById("rep").lastElementChild.value);
        input.setAttribute("value", repValue);
    }
    var br = $("<br>");
    rep.append(br);
    rep.append(input);
    tabIndexNum++;

    //Resistance Input
    var input = document.createElement("input");
    input.setAttribute("type", "number");
    input.setAttribute("name", resistanceName);
    input.setAttribute("tabindex", tabIndexNum);
    input.setAttribute("autocomplete", "off");
    if(document.getElementById("resistance").firstChild){
        let resistanceValue = parseInt(document.getElementById("resistance").lastElementChild.value);
        input.setAttribute("value", resistanceValue);
    }
    var br = $("<br>");
    resistance.append(br);
    resistance.append(input);
    tabIndexNum++;

    addEvents();
}

function addEvents(){
    let items = document.querySelectorAll("input")
    items.forEach(e => {
        if(e.hasAttribute("special")){
            e.addEventListener("input", changeSetNumber)
        }
    })
}

function changeSetNumber(e){
    let tabIndex = e.target.getAttribute('tabindex');
    tabIndex++;
    let inputToChange = document.querySelectorAll('input');
    inputToChange.forEach(element => {
        if (element.getAttribute("tabindex") == tabIndex){
            element.value = 1;
        }
    });
}

//Depriciated used for loading a list of workouts into a select2 input that did not work
var workout_lst = [];
function load_workout_lst(lst){
    for (let i = 0; i < lst.length; i++){
        workout_lst.push(lst[i]);
    }
}