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
    
    var inputDrop = document.createElement("input");
    inputDrop.setAttribute("name", exerciseName);
    inputDrop.setAttribute("tabindex", tabIndexNum);
    if(document.getElementById("exercise").firstChild){
        let exerciseValue = document.getElementById("exercise").lastElementChild.value;
        inputDrop.setAttribute("value", exerciseValue);
    }
    // var input = $("<select>").attr("type", "text").attr("name", exerciseName).attr("tabindex", tabIndexNum);  
    // for(var i = 0, l = workout_lst.length; i < l; i++){
    //     console.log(workout_lst[i]);
    //     var item = workout_lst[i];
    //     inputDrop.options.add(new Option(item));
    // }
    var br = $("<br>");
    exercise.append(br);
    exercise.append(inputDrop);
    // inputDrop.select2();
    tabIndexNum++;
    inputDrop.focus();

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
// function trackInputs(){
//     document.getElementById('addRowButton').disabled = true;
//     let inputs = document.getElementsByTagName("input");
//     for (let index = 0; index < inputs.length; index++) {
//         inputs[index].addEventListener("input", checkFilled);
//     }
// }

// function checkFilled(){
//     let inputs = document.getElementsByTagName("input");
//     let count = inputs.length;
//     let testCount = 0;
//     for (let index = 0; index < count; index++) {
//         if (inputs[index].value !== "") {
//             testCount += 1;
//         }
//     }
//     if (testCount == count){
//         document.getElementById('addRowButton').removeAttribute("disabled");
//     }
// }

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
var workout_lst = [];

function load_workout_lst(lst){
    for (let i = 0; i < lst.length; i++){
        workout_lst.push(lst[i]);
    }
}

// addInitialRow();
let exercisesTop = document.getElementById("exercise");
// exercisesTop.children[1].addEventListener("input", changeSetNumber);