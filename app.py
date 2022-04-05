import threading
from flask import Flask, request, Response
from flask_cors import CORS
import json

from bot import Bot

app = Flask(__name__)
CORS(app) # Allow cross origin requests

users = {}

# Start bot function
@app.route('/start',methods = ['POST'])
def start():
    if request.method == 'POST':
        
        try:
            data = request.json

            balance = int(data["balance"])
            symbols = list(data["symbols"])
            user = str(data["user"])

            bot = Bot(user, balance, symbols)

            # Add the bot to a dictionary to retrieve later when getting info in the getData method
            users[user] = bot

            # Use a thread to allow multiple bots to run simultaneously
            threading.Thread(target=bot.run, name=user).start()

            return Response(json.dumps({'status' : 1}), mimetype='application/json')
        
        except:
            return Response(json.dumps({'status' : -1}), mimetype='application/json')
        
        # Get bot data function
@app.route("/get", methods = ['POST'])
def getData():
    if request.method == 'POST':
        try:
            data = request.json
            currentUser = str(data['user'])

            if currentUser in users:
            
                # Get the current users bot
                bot = users[currentUser]

                if bot.running:
                    env = bot.env

                    data = {
                        'data': env.data,
                        'prices': bot.prices,
                        'running': True,
                        'issue': False
                    }

                    return Response(json.dumps(data), mimetype='application/json')

                else:
                    env = bot.env
                    
                    data = {
                        'data': env.data,
                        'running': False,
                        'issue': False
                    }
                    
                    # Remove the bot from the list if its not running
                    print(f"Removing {bot.user}")
                    users.pop(currentUser)
                    
                    return Response(json.dumps(data), mimetype='application/json')
            else:
                return Response(json.dumps({'issue': True}), mimetype='application/json')
        except Exception:
            return Response(json.dumps({'issue': True, 'message': 'error'}), mimetype='application/json')

            
 
