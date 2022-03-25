let finished = false;
let buys = [];
let sells = [];

let balance = 1000;
let bot_funds = 2000;

// let API_URL = "http://192.168.1.4:5000/";
let API_URL = "https://tradingbotlk.herokuapp.com/"

window.addEventListener("load", function() {

    var xValues = ["Start"];
    var yValues = [bot_funds];

    var chart = new Chart("chart", {
        type: "line",
        data: {
            labels: xValues,
            datasets: [
            {
                fill: false,
                lineTension: 0,
                backgroundColor: "rgb(0, 0, 0)",
                // borderColor: "rgba(108, 122, 137, 0.5)",
                borderColor: "#aaa",
                data: yValues
            }]
        },
        options: {
            legend: {display: false},
            scales: {
                yAxes: [{
                    ticks: {
                        fontColor: "#ccc"
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Equity',
                        fontColor: "#ccc"
                    }
                }],
                xAxes: [{
                    ticks: {
                        fontColor: "#ccc"
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Date',
                        fontColor: "#ccc"
                    }
                }]
            }
        }
    });

    document.getElementById("start").addEventListener("click", function() {
    
        let amount = document.getElementById("amount").value;

        startBot();
    
        if(!isNaN(amount)) startBot();
        else alert("Enter a valid amount");
    });
    
    // startBot();
    
    let timer = setInterval(function() {

        if(finished && sells.length == 9) {
            clearInterval(timer);
            console.log("finished");
            console.log(buys);
            console.log(sells);
        } 

        else {
            getData(chart);
        }
        
    }, 1000);

});

function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}

function startBot() {

    console.log("Bot Start")

    let data =
    {
        balance: balance,
        symbols: ["A", "AAPL", "GOOG", "FB"]
    }

    fetch(API_URL + 'start', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
        })
        .then(response => {
            finished = true;
        })
        .catch((error) => {
        console.error('Error:', error);
    });
}

let bought = false;

function getData(chart) {

    fetch(API_URL + 'get')
    // Handle success
    .then(response => response.json())  // convert to json
    .then(json => {

        if(!bought && buys.length != json.buys.length) {
            buys.push(json.buys[json.buys.length - 1]);

            bot_funds = bot_funds - json.buys[json.buys.length - 1][2]

            addData(chart, json.buys[json.buys.length - 1][1], bot_funds);

            console.log(json.buys[json.buys.length - 1], balance, "buy");

            bought = true;

            let template =
                `<tr>
                    <td>`+ json.buys[json.buys.length - 1][1] +`</td>
                    <td>USD `+ json.buys[json.buys.length - 1][3] +`</td>
                    <td>`+ json.buys[json.buys.length - 1][4] +`</td>
                    <td>BUY</td>
                </tr>`;

            document.getElementById("history-table").innerHTML += template;

        }

        if(bought && sells.length != json.sells.length) {
            sells.push(json.sells[json.sells.length - 1]);

            bot_funds = bot_funds + json.sells[json.sells.length - 1][2]

            addData(chart, json.sells[json.sells.length - 1][1], bot_funds);

            console.log(json.sells[json.sells.length - 1], balance, "sell");

            bought = false;

            let template =
                `<tr>
                    <td>`+ json.sells[json.sells.length - 1][1] +`</td>
                    <td>USD `+ json.sells[json.sells.length - 1][3] +`</td>
                    <td>`+ json.sells[json.sells.length - 1][4] +`</td>
                    <td>SELL</td>
                </tr>`;

            document.getElementById("history-table").innerHTML += template;

        }

    })    
    .catch(err => console.log('Request Failed', err)); // Catch errors

}