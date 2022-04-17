// Parse JSON data
// const json = '{{graph_exercises | safe | replace("\\", "")}}';
// const obj = JSON.parse(json);
let json;
let obj;
// Get chart to update with drop down options
async function updateChart(dropdown){
    const exercise = obj.exercises;
    
    const date = exercise[dropdown.value].map(
        function(index){
            return index.workout_date;
        }
    );
    const data = exercise[dropdown.value].map(
        function(index){
            return index.resistance;
        }
    );
    myChart.data.labels = date;
    myChart.data.datasets[0].label = dropdown.value;
    myChart.data.datasets[0].data = data;

    myChart.update();
}

// setup 
let data = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [{
    label: 'Weekly Sales',
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
