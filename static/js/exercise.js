var dateTimeName = "nDatetime[]"
var exerciseName = "nExercise[]"
var setNumberName = "nSetnumber[]"
var repName = "nRep[]"
var resistanceName = "nResistance[]"

function addRow(){
    let datetimeValue = document.getElementById("datetime").lastElementChild.value;
    let datetime = $("#datetime");
    var input;
    var input = $("<input>").attr("type", "datetime-local").attr("name", dateTimeName).attr("value", datetimeValue).attr("tabindex", tabIndexNum).attr("autocomplete", "off");  
    var br = $("<br>");
    datetime.append(br);
    datetime.append(input);
    tabIndexNum++;
    
    let exerciseValue = document.getElementById("exercise").lastElementChild.value;
    let exercise = $("#exercise");
    var input;
    var input = $("<input>").attr("type", "text").attr("name", exerciseName).attr("value", exerciseValue).attr("tabindex", tabIndexNum).attr("autocomplete", "off");  
    var br = $("<br>");
    exercise.append(br);
    exercise.append(input);
    input.focus();
    tabIndexNum++;

    let setNumberValue = parseInt(document.getElementById("setnumber").lastElementChild.value) + 1;
    let setNumber = $("#setnumber");
    var input;
    var input = $("<input>").attr("type", "number").attr("name", setNumberName).attr("value", setNumberValue).attr("tabindex", tabIndexNum).attr("autocomplete", "off");  
    var br = $("<br>");
    setNumber.append(br);
    setNumber.append(input);
    tabIndexNum++;

    let repValue = parseInt(document.getElementById("rep").lastElementChild.value);
    let rep = $("#rep")
    var input;
    var input = $("<input>").attr("type", "number").attr("name", repName).attr("value", repValue).attr("tabindex", tabIndexNum).attr("autocomplete", "off");  
    var br = $("<br>");
    rep.append(br);
    rep.append(input);
    tabIndexNum++;

    let resistanceValue = parseInt(document.getElementById("resistance").lastElementChild.value);
    let resistance = $("#resistance")
    var input;
    var input = $("<input>").attr("type", "number").attr("name", resistanceName).attr("step", ".5").attr("value", resistanceValue).attr("tabindex", tabIndexNum).attr("autocomplete", "off");  
    var br = $("<br>");
    resistance.append(br);
    resistance.append(input);
    tabIndexNum++;

}

function trackInputs(){
    let inputs = document.getElementsByTagName("input");
    for (let index = 0; index < inputs.length; index++) {
        inputs[index].addEventListener("input", checkFilled);
    }
}

function checkFilled(){
    let inputs = document.getElementsByTagName("input");
    let count = inputs.length;
    let testCount = 0;
    for (let index = 0; index < count; index++) {
        if (inputs[index].value !== "") {
            testCount += 1;
        }
    }
    if (testCount == count){
        document.getElementById('addCap').removeAttribute("disabled");
    }
}

let tabIndexNum = 1;
function addInitialRow(){
    let datetime = $("#datetime");
    var input;
    var input = $("<input>").attr("type", "datetime-local").attr("name", dateTimeName).attr("tabindex", tabIndexNum).attr("autocomplete", "off");  
    var br = $("<br>");
    datetime.append(br);
    datetime.append(input);
    tabIndexNum++;

    let exercise = $("#exercise");
    var input;
    var input = $("<input>").attr("type", "text").attr("name", exerciseName).attr("tabindex", tabIndexNum).attr("autocomplete", "off");  
    var br = $("<br>");
    exercise.append(br);
    exercise.append(input);
    tabIndexNum++;

    let setNumber = $("#setnumber");
    var input;
    var input = $("<input>").attr("type", "number").attr("name", setNumberName).attr("tabindex", tabIndexNum).attr("autocomplete", "off");
    var br = $("<br>");
    setNumber.append(br);
    setNumber.append(input);
    tabIndexNum++;

    let rep = $("#rep")
    var input;
    var input = $("<input>").attr("type", "number").attr("name", repName).attr("tabindex", tabIndexNum).attr("autocomplete", "off");
    var br = $("<br>");
    rep.append(br);
    rep.append(input);
    tabIndexNum++;

    let resistance = $("#resistance")
    var input;
    var input = $("<input>").attr("type", "number").attr("name", resistanceName).attr("step", ".5").attr("tabindex", tabIndexNum).attr("autocomplete", "off");
    var br = $("<br>");
    resistance.append(br);
    resistance.append(input);
    tabIndexNum++;

    trackInputs();
}

addInitialRow();