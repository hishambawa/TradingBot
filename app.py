from crypt import methods
import threading
from flask import Flask, request, Response
from flask_cors import CORS
import json

from bot import Bot

app = Flask(__name__, static_folder='frontend', static_url_path='')
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
             return Response(json.dumps({'issue': True, 'message': 'error'}), mimetype='application/json')
            
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

 # Stop bot function
@app.route("/stop", methods = ['POST'])
def stop():
    if request.method == 'POST':
        try:
            user = str(request.json['user'])
                       
            for thread in threading.enumerate():
                
                # Check if a thread with the name of the user who want to stop the bot exists
                if thread.name == user:

                    # Set the force_stop variable of the thread to True. This will stop the bot
                    # as the bot constantly checks the value of this variable, and only continues if
                    # it is set to False.
                    thread.force_stop = True
                    
                    # Remove the user from the dictionary after stopping the bot
                    print(f"Removing {user}")
                    users.pop(user)
                    
                    return Response(json.dumps({'status' : 1}), mimetype='application/json')
                
            return Response(json.dumps({'status' : 0, 'message': f'couldnt find thread {user}'}), mimetype='application/json')

        except Exception:
            return Response(json.dumps({'status' : -1}), mimetype='application/json')

# Check the app version
@app.route("/version", methods = ['GET'])
def version():
    return Response(json.dumps({'version' : 1.0}), mimetype='application/json')

# Run flask on all public IP addresses
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
