function addRow(){
    // Disable button
    document.getElementById("addCap").disabled = true;

    // Add a new row to exercises
    let datetime = $("#datetime");
    var input;
    var input = $("<input>").attr("type", "datetime-local").attr("name", "ndatetime[]");  
    var br = $("<br>");
    datetime.append(br);
    datetime.append(input);

    let exercise = $("#exercise");
    var input;
    var input = $("<input>").attr("type", "text").attr("name", "nExercise[]");  
    var br = $("<br>");
    exercise.append(br);
    exercise.append(input);

    let setNumber = $("#setnumber");
    var input;
    var input = $("<input>").attr("type", "number").attr("name", "nsetnumber[]");  
    var br = $("<br>");
    setNumber.append(br);
    setNumber.append(input);

    let rep = $("#rep")
    var input;
    var input = $("<input>").attr("type", "number").attr("name", "nrep[]");  
    var br = $("<br>");
    rep.append(br);
    rep.append(input);

    let resistance = $("#resistance")
    var input;
    var input = $("<input>").attr("type", "number").attr("name", "nresistance[]").attr("step", ".5");  
    var br = $("<br>");
    resistance.append(br);
    resistance.append(input);
    addInputs();
}

function addInputs(){
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
        alert("All filled");
        document.getElementById('addCap').removeAttribute("disabled");
    }
}

addInputs();