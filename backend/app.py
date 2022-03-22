from flask import Flask, request, Response
from flask_cors import CORS
import json

from bot import Bot

app = Flask(__name__)
CORS(app) # Allow cross origin requests

@app.route('/start',methods = ['POST'])
def login():
    if request.method == 'POST':
        data = request.json
        balance = int(data["balance"])
        symbols = list(data["symbols"])

        global trade_bot

        trade_bot = Bot(balance, symbols)
        trade_bot.run()

        return "done"

@app.route("/get", methods = ['GET'])
def getBuys():
    try:
        env = trade_bot.env

        data = {
            'buys': env.stock_buys,
            'sells' : env.stock_sells
        }

        return Response(json.dumps(data), mimetype='application/json')
    except:
        return "An error occurred"

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
