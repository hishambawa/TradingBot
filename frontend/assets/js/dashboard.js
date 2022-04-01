let buys = [];
let sells = [];

let bot_funds = 10000;
let initial_funds = 0;
let bot_leftovers = 0;
let previous_pl = 0;
let index = 0;

let API_URL = "https://tradingbotlk.herokuapp.com/";
let user = sessionStorage.getItem("user");

let chart;
let running = false;

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
                        labelString: 'Period',
                        fontColor: "#ccc"
                    }
                }]
            }
        }
    });

    document.getElementById("start").addEventListener("click", function() {
        initial_funds = document.getElementById("amount").value;
        bot_leftovers = bot_funds - initial_funds;
    
        if(!isNaN(initial_funds) && initial_funds != "" && initial_funds <= bot_funds) startBot(initial_funds);
        else if (initial_funds > bot_funds) alert("Insufficient funds");
        else alert("Enter a valid amount");
    });

    this.document.getElementById("stop").addEventListener("click", function() {
        stopBot();
    })
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
        .then(response => response.json())
        .then(json => {
            if(json.status == 1) index = 0;
            else errorHandler('startBot', json);
        })
        .catch((error) => errorHandler('startBot', error));

    let timer = setInterval(function() {

        if(running){
            getData(chart);
        }

        else {
            clearInterval(timer);

            // Show the amount and start bot button and hide the stop bot button when the bot is done
            document.getElementById("stop").style.display = "none";
            document.getElementById("start").style.display = "block";
            document.getElementById("amount").style.display = "block";
            document.getElementById("amount").value = "";

            // Save the profit/loss after the bot stops to continue from here when restarting the bot
            previous_pl = parseFloat(document.getElementById("profit-loss").innerText);
        }
        
    }, 1000);
}

function stopBot() {
    fetch(API_URL + 'stop', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({'user': user}),
        })
        .then(response => response.json())
        .then(json => {
            if(json.status == 1) running = false;
            else if(json.status == 0) stopBot();
            else errorHandler('stopBot', json);
        })
        .catch((error) => {
            errorHandler('stopBot', error);
    });
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
    .then(response => response.json())
    .then(json => {

        if(!json.issue) {
            // Check if the bot is running
            if(!json.running) {
                running = false;
            }

            // Check if the bot is running AND if json.data is not empty
            // json.data returns a json array with all the buys and sells of the bot in order
            else if(json.data.length > index && json.running) {

                // Check if the action is 'buy' and if the index is 0 (this is always a buy) OR if the data in the current index already exists in the buys array 
                if(json.data[index].action == 'buy' && (index == 0 || !includes(buys, json.data[index].time))) {
        
                    buys.push(json.data[index]);
    
                    bot_funds = bot_funds - json.data[index].value;
                    addData(chart, json.data[index].time, bot_funds); // Update the chart
    
                    let template =
                    `<tr>
                        <td>`+ json.data[index].time +`</td>
                        <td>`+ json.data[index].symbol +`</td>
                        <td>$`+ json.data[index].price +`</td>
                        <td>`+ json.data[index].quantity +`</td>
                        <td class='buy'>BUY</td>
                    </tr>`;
    
                    document.getElementById("history-table").innerHTML += template; // Update the history table
                    document.getElementById("equity").innerText = bot_funds.toLocaleString(undefined, {maximumFractionDigits: 2}); // Round off and add commas
    
                    index++;
                }
        
                // Check if the action is 'sell' and if the index is 1 (this is always a sell) OR if the data in the current index already exists in the sells array 
                if(json.data[index].action == 'sell' && (index == 1 || !includes(sells, json.data[index].time))) {
        
                    sells.push(json.data[index]);
    
                    bot_funds = bot_funds + json.data[index].value;
                    addData(chart, json.data[index].time, bot_funds); // Update the chart
    
                    let template =
                    `<tr>
                        <td>`+ json.data[index].time +`</td>
                        <td>`+ json.data[index].symbol +`</td>
                        <td>$`+ json.data[index].price +`</td>
                        <td>`+ json.data[index].quantity +`</td>
                        <td class='sell'>SELL</td>
                    </tr>`;
    
                    document.getElementById("history-table").innerHTML += template; // Update the history table
                    document.getElementById("equity").innerText = bot_funds.toLocaleString(undefined, {maximumFractionDigits: 2}); // Round off and add commas
    
                    index++;

                    // Get the earnings from the portion of funds used by the bot
                    let bot_earnings = bot_funds - bot_leftovers;

                    // Update the total profit/loss percentage
                    let earnings = ((bot_earnings - initial_funds) / initial_funds) * 100; // Calculate the profit/loss for the current period

                    if(previous_pl != 0) earnings += previous_pl; // If the bot ran before, add the previous profit/loss to the current period

                    document.getElementById("profit-loss").innerText = earnings.toFixed(2); // Update the profit/loss

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

            // Update the prices of stocks
            document.getElementById("price-table").innerHTML = "";

            for(symbol in json.prices) {
                let prices =
                `<tr>
                    <td>`+ symbol +`</td>
                    <td>$`+ json.prices[symbol].toLocaleString(undefined, {maximumFractionDigits: 2}) +`</td>
                </tr>`;

                document.getElementById("price-table").innerHTML += prices;
            }
        }
    })    
    .catch(error => console.log(error));
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

// Save the error details in the session storage and redirect to an error page
function errorHandler(cause, error) {
    sessionStorage.setItem("error", error);
    window.location.href = "error.html?cause=" + cause;
}