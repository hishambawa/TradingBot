let buys = [];
let sells = [];

let bot_funds = 10000;
let initial_funds = 0;
let bot_leftovers = 0;

let user = sessionStorage.getItem("user");
let running;

let index = 0;

let chart;

let API_URL = "https://tradingbotlk.herokuapp.com/";

window.addEventListener("load", function() {

    // Check if a user is in the session. Else return to the login page
    if(user == null) {
        window.location.href = "index.html";
    }

    var xValues = ["Start"];
    var yValues = [bot_funds];

    chart = new Chart("chart", {
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
        initial_funds = document.getElementById("amount").value;
        
        bot_leftovers = bot_funds - initial_funds;
    
        if(!isNaN(initial_funds) && initial_funds != "") startBot(initial_funds);
        else alert("Enter a valid amount");
    });
});

function startBot(amount) {

    // Hide the amount and stop bot button and show the stop bot button when running the bot
    document.getElementById("amount").style.display = "none";
    document.getElementById("start").style.display = "none";
    document.getElementById("stop").style.display = "block";

    running = true;

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
            index = 0;
        })
        .catch((error) => {
            console.error('Error:', error);
            running = false;
    });

    let timer = setInterval(function() {

        if(running){
            getData(chart);
        }

        else {
            clearInterval(timer);
            console.log("finished");

            // Show the amount and start bot button and hide the stop bot button when the bot is done
            document.getElementById("stop").style.display = "none";
            document.getElementById("start").style.display = "block";
            document.getElementById("amount").style.display = "block";
        }
        
    }, 1000);
}

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

        if(!json.issue) {
            // Check if the bot is running
            if(!json.running) {
                running = false;
            }

            else if(json.data.length > index && json.running) {
                if(json.data[index].action == 'buy') {
        
                    if(index == 0 || !includes(buys, json.data[index].time)) {

                        buys.push(json.data[index]);
        
                        bot_funds = bot_funds - json.data[index].value;
                        addData(chart, json.data[index].time, bot_funds);
        
                        let template =
                        `<tr>
                            <td>`+ json.data[index].time +`</td>
                            <td>`+ json.data[index].symbol +`</td>
                            <td>USD `+ json.data[index].price +`</td>
                            <td>`+ json.data[index].quantity +`</td>
                            <td class='buy'>BUY</td>
                        </tr>`;
        
                        document.getElementById("history-table").innerHTML += template;
                        document.getElementById("equity").innerText = bot_funds.toLocaleString(undefined, {maximumFractionDigits: 2}); // Round off and add commas
        
                        index++;
                    }
                }
        
                if(json.data.length > index && json.data[index].action == 'sell') {
        
                    if(index == 1 || !includes(sells, json.data[index].time)) {

                        sells.push(json.data[index]);
        
                        bot_funds = bot_funds + json.data[index].value;
                        addData(chart, json.data[index].time, bot_funds);
        
                        let template =
                        `<tr>
                            <td>`+ json.data[index].time +`</td>
                            <td>`+ json.data[index].symbol +`</td>
                            <td>USD `+ json.data[index].price +`</td>
                            <td>`+ json.data[index].quantity +`</td>
                            <td class='sell'>SELL</td>
                        </tr>`;
        
                        document.getElementById("history-table").innerHTML += template;
                        document.getElementById("equity").innerText = bot_funds.toLocaleString(undefined, {maximumFractionDigits: 2}); // Round off and add commas
        
                        index++;

                        // Get the portion of funds that was used in the bot
                        let bot_funds_used = bot_funds - bot_leftovers;

                        // Update the total profit/loss percentage
                        let earnings = ((bot_funds_used - initial_funds) / initial_funds) * 100; 
                        document.getElementById("profit-loss").innerText = earnings.toFixed(2);

                        // Set the color of the total profit/loss as green if the earning % is a positive value. Else set the color to red
                        if(earnings < 0) {
                            document.getElementById("profit-loss").classList.add("loss");
                            document.getElementById("profit-loss").classList.remove("profit");
                        }

                        else {
                            document.getElementById("profit-loss").classList.remove("loss");
                            document.getElementById("profit-loss").classList.add("profit");
                        }
                    }
                }

            }

            // Update the prices of stocks
            document.getElementById("price-table").innerHTML = "";

            for(symbol in json.prices) {
                let prices =
                `<tr>
                    <td>`+ symbol +`</td>
                    <td>`+ json.prices[symbol] +`</td>
                </tr>`;

                document.getElementById("price-table").innerHTML += prices;
            }
        }

    })    
    .catch(err => console.log('Request Failed', err)); // Catch errors

}

function logout() {
    sessionStorage.clear();
    window.location.href = "index.html";
}

// Check if an element is included in an array
function includes(array, value) {
    for(item of array) {
        if(item.time == value.time) return true;
    }

    return false;
}

// Add data to the chart
function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}