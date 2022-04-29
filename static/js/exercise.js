function addRow(){
    // Add a new row to exercises
    let datetimeValue = document.getElementById("datetime").lastElementChild.value;
    let datetime = $("#datetime");
    var input;
    var input = $("<input>").attr("type", "datetime-local").attr("name", "nDatetime[]").attr("value", datetimeValue);  
    var br = $("<br>");
    datetime.append(br);
    datetime.append(input);
    
    let exerciseValue = document.getElementById("exercise").lastElementChild.value;
    let exercise = $("#exercise");
    var input;
    var input = $("<input>").attr("type", "text").attr("name", "nExercise[]").attr("value", exerciseValue);  
    var br = $("<br>");
    exercise.append(br);
    exercise.append(input);

    let setNumberValue = parseInt(document.getElementById("setnumber").lastElementChild.value) + 1;
    let setNumber = $("#setnumber");
    var input;
    var input = $("<input>").attr("type", "number").attr("name", "nSetnumber[]").attr("value", setNumberValue);  
    var br = $("<br>");
    setNumber.append(br);
    setNumber.append(input);

    let repValue = parseInt(document.getElementById("rep").lastElementChild.value);
    let rep = $("#rep")
    var input;
    var input = $("<input>").attr("type", "number").attr("name", "nRep[]").attr("value", repValue);  
    var br = $("<br>");
    rep.append(br);
    rep.append(input);

    let resistanceValue = parseInt(document.getElementById("resistance").lastElementChild.value);
    let resistance = $("#resistance")
    var input;
    var input = $("<input>").attr("type", "number").attr("name", "nResistance[]").attr("step", ".5").attr("value", resistanceValue);  
    var br = $("<br>");
    resistance.append(br);
    resistance.append(input);
    trackInputs();
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

trackInputs();
addRow();