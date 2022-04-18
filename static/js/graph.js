let json;
let obj;
let exercise_name;

let mainColor;
let mainColorSide;
let secondColor;
let secondColorSide;

function initColors(color1, alpha1, color2, alpha2, color3, alpha3, color4, alpha4){
    mainColor = hexToRGB(color1, alpha1);
    mainColorSide = hexToRGB(color2, alpha2);
    secondColor = hexToRGB(color3, alpha3);
    secondColorSide = hexToRGB(color4, alpha4);
}
// Get chart to update with drop down options
async function updateChart(dropdown){
    const exercise = obj.exercises;
    
    const date = exercise[dropdown.value].map(
        function(index){
            date_lst = index.workout_date;
            let date_modded = date_lst.replace("T", " ");
            return date_modded;
        }
    );
    const data_resistance = exercise[dropdown.value].map(
        function(index){
            return index.resistance;
        }
    );
    const data_interval = exercise[dropdown.value].map(
        function(index){
            return index.interval;
        }
    );
    myChart.data.labels = date;
    myChart.data.datasets[0].data = data_resistance;
    myChart.data.datasets[0].backgroundColor = [mainColor];
    myChart.data.datasets[0].borderColor = [mainColorSide];
    myChart.data.datasets[1].data = data_interval;
    myChart.data.datasets[1].backgroundColor = [secondColor];
    myChart.data.datasets[1].borderColor = [secondColorSide];
    exercise_name.innerHTML = dropdown.value;
    myChart.update();
}

function hexToRGB(hex, alpha) {
    var r = parseInt(hex.slice(1, 3), 16),
        g = parseInt(hex.slice(3, 5), 16),
        b = parseInt(hex.slice(5, 7), 16);

    if (alpha) {
        return "rgba(" + r + ", " + g + ", " + b + ", " + alpha + ")";
    } else {
        return "rgb(" + r + ", " + g + ", " + b + ")";
    }
}

let data = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [{
        label: 'Resistance',
        data: [18, 12, 6, 9, 12, 3, 9],
        backgroundColor: [
            'rgba(255, 26, 104, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(0, 0, 0, 0.2)'
        ],
        borderColor: [
            'rgba(255, 26, 104, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(0, 0, 0, 1)'
        ],
        borderWidth: 1
    },
    {
        type: 'bar',
        label: 'Intervals',
        data: [18, 12, 6, 9, 12, 3, 9],
        backgroundColor: [
            'rgba(255, 26, 104, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(0, 0, 0, 0.2)'
        ],
        borderColor: [
            'rgba(255, 26, 104, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(0, 0, 0, 1)'
        ],
        borderWidth: 1
    }]
};

// config 
const config = {
    type: 'line',
    data,
    options: {
    scales: {
        y: {
        beginAtZero: true
        }
    }
    }
};

// render init block
const myChart = new Chart(
    document.getElementById('myChart'),
    config
);
