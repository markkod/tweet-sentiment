import socket
from flask import Flask, render_template, request, Response, send_from_directory
import json
import requests


app = Flask(__name__, static_url_path="", static_folder='static')
app.debug = True

tweet_queue = []

hashtags = []

def tweet_stream():
    print("Stream started")
    while True:
        if(len(tweet_queue) > 0):
            tweet_data = json.dumps(tweet_queue.pop(0))
            print(tweet_data)
            yield "data: {}\n\n".format(tweet_data)

@app.route('/')
def hello():
    return render_template('dashboard.html')


@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('templates', path)


@app.route("/data", methods=["POST"])
def newData():
    global tweet_queue
    print(request.json)
    json_data = json.loads(request.json)
    label = json_data["label"]
    coordinates = json_data["coordinates"]
    tweet_queue.append(json_data)

    print("Got label {0} with coordinates {1}".format(label, coordinates))

    return "Got data"




@app.route('/stream')
def stream():
    return Response(tweet_stream(), mimetype="text/event-stream")


@app.route("/hashtags", methods=["GET", "POST"])
def getHashtags():
    global hashtags
    if request.method == "GET":
        response = {"hashtags": hashtags}
        return response
    elif request.method == "POST":
        hashtags = request.json["hashtags"]
        requests.post('http://localhost:5000/addhashtags', json=request.json)
        print(hashtags)
        return "success"


if __name__ == '__main__':
    app.run(threaded=True, port=5001)
