let finished = false;
let buys = [];
let sells = [];

// let balance = 1000;
let bot_funds = 10000;

let user = sessionStorage.getItem("user");
let running = false;

let index = 0;

// let API_URL = "http://192.168.1.4:5000/";
// let API_URL = "http://192.168.1.4:5000/";
let API_URL = "https://tradingbotlk.herokuapp.com/";

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

        console.log(amount);
    
        if(!isNaN(amount) && amount != "") startBot(amount);
        else alert("Enter a valid amount");
    });
        
    let timer = setInterval(function() {

        if(finished) {
            clearInterval(timer);
            console.log("finished");
        } 

        if(running){
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

function startBot(amount) {

    console.log("Bot Start")

    let data =
    {
        balance: amount,
        symbols: ["A", "AAPL", "GOOG", "FB"],
        user: user
    }

    fetch(API_URL + 'start', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
        })
        .then(response => {
            running = true;
        })
        .catch((error) => {
        console.error('Error:', error);
    });
}

let bought = false;

function getData(chart) {

    let data = { user: user};

    fetch(API_URL + 'get', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    // Handle success
    .then(response => response.json())  // convert to json
    .then(json => {

        console.log(json);

        // Check if the bot is running
        if(json.data[index] != null && !json.data[index].running) {
            running = false;
            finished = true;
        }

        else if(json.data[index] != null && json.data[index].running) {
            if(json.data[index].action == 'buy') {
    
                if(index == 0 || !includes(buys, json.data[index].time)) {
                    console.log('buy');

                    buys.push(json.data[index]);
    
                    bot_funds = bot_funds - json.data[index].value;
                    addData(chart, json.data[index].time, bot_funds);
    
                    let template =
                    `<tr>
                        <td>`+ json.data[index].time +`</td>
                        <td>USD `+ json.data[index].price +`</td>
                        <td>`+ json.data[index].quantity +`</td>
                        <td>BUY</td>
                    </tr>`;
    
                    document.getElementById("history-table").innerHTML += template;
    
                    index++;
                }
            }
    
            if(json.data[index] != null && json.data[index].action == 'sell') {
    
                if(index == 1 || !includes(sells, json.data[index].time)) {
                    console.log('sell');

                    sells.push(json.data[index]);
    
                    bot_funds = bot_funds + json.data[index].value;
                    addData(chart, json.data[index].time, bot_funds);
    
                    let template =
                    `<tr>
                        <td>`+ json.data[index].time +`</td>
                        <td>USD `+ json.data[index].price +`</td>
                        <td>`+ json.data[index].quantity +`</td>
                        <td>SELL</td>
                    </tr>`;
    
                    document.getElementById("history-table").innerHTML += template;
    
                    index++;
                }
            }

        }

        // Update the prices
        document.getElementById("price-table").innerHTML = 
            `<tr>
                <th>Price</th>
                <th>Symbol</th>
            </tr>`;

            for(symbol in json.prices) {
                let prices =
                `<tr>
                    <td>`+ json.prices[symbol] +`</td>
                    <td>`+ symbol +`</td>
                </tr>`;

                document.getElementById("price-table").innerHTML += prices;
            }

    })    
    .catch(err => console.log('Request Failed', err)); // Catch errors

}

function includes(array, value) {
    for(item of array) {
        if(item.time == value.time) return true;
    }

    return false;
}

function logout() {

    sessionStorage.clear();
    window.location.href = "index.html";
}