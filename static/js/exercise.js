var dateTimeName = "nDatetime[]"
var exerciseName = "nExercise[]"
var setNumberName = "nSetnumber[]"
var repName = "nRep[]"
var resistanceName = "nResistance[]"

function addRow(){
    let datetimeValue = document.getElementById("datetime").lastElementChild.value;
    let datetime = $("#datetime");
    var input;
    var input = $("<input>").attr("type", "datetime-local").attr("name", dateTimeName).attr("value", datetimeValue);  
    var br = $("<br>");
    datetime.append(br);
    datetime.append(input);
    
    let exerciseValue = document.getElementById("exercise").lastElementChild.value;
    let exercise = $("#exercise");
    var input;
    var input = $("<input>").attr("type", "text").attr("name", exerciseName).attr("value", exerciseValue);  
    var br = $("<br>");
    exercise.append(br);
    exercise.append(input);

    let setNumberValue = parseInt(document.getElementById("setnumber").lastElementChild.value) + 1;
    let setNumber = $("#setnumber");
    var input;
    var input = $("<input>").attr("type", "number").attr("name", setNumberName).attr("value", setNumberValue);  
    var br = $("<br>");
    setNumber.append(br);
    setNumber.append(input);

    let repValue = parseInt(document.getElementById("rep").lastElementChild.value);
    let rep = $("#rep")
    var input;
    var input = $("<input>").attr("type", "number").attr("name", repName).attr("value", repValue);  
    var br = $("<br>");
    rep.append(br);
    rep.append(input);

    let resistanceValue = parseInt(document.getElementById("resistance").lastElementChild.value);
    let resistance = $("#resistance")
    var input;
    var input = $("<input>").attr("type", "number").attr("name", resistanceName).attr("step", ".5").attr("value", resistanceValue);  
    var br = $("<br>");
    resistance.append(br);
    resistance.append(input);
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

function addInitialRow(){
    let datetime = $("#datetime");
    var input;
    var input = $("<input>").attr("type", "datetime-local").attr("name", dateTimeName);  
    var br = $("<br>");
    datetime.append(br);
    datetime.append(input);
    
    let exercise = $("#exercise");
    var input;
    var input = $("<input>").attr("type", "text").attr("name", exerciseName);  
    var br = $("<br>");
    exercise.append(br);
    exercise.append(input);

    let setNumber = $("#setnumber");
    var input;
    var input = $("<input>").attr("type", "number").attr("name", setNumberName);
    var br = $("<br>");
    setNumber.append(br);
    setNumber.append(input);

    let rep = $("#rep")
    var input;
    var input = $("<input>").attr("type", "number").attr("name", repName)
    var br = $("<br>");
    rep.append(br);
    rep.append(input);

    let resistance = $("#resistance")
    var input;
    var input = $("<input>").attr("type", "number").attr("name", resistanceName).attr("step", ".5");
    var br = $("<br>");
    resistance.append(br);
    resistance.append(input);
    trackInputs();
}

addInitialRow();