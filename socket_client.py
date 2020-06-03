import socket
from queue import Queue
from flask import Flask, render_template, request, Response, send_from_directory

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9009        # The port used by the server

app = Flask(__name__, static_url_path="", static_folder='static')
app.debug = True

queue = Queue()

hashtags = ["#sunset", "#horse", "#dogsofinstagram", "#travel", "#location", "#party", "#event", "#like"]



def tweet_stream():
    print("Stream started")
    s = socket.socket()
    s.connect((HOST, PORT))
    print(s)
    while True:
        print("Test")
        data = s.recv(1024)
        print('Received', repr(data))
        yield "data: {}\n\n".format(data)


@app.route('/')
def hello():
    return render_template('dashboard.html')

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('templates', path)



@app.route('/stream')
def stream():
    # create a new socket and connect to it
    # s = socket.socket()
    # s.connect((HOST, PORT))
    # print(s)
    return Response(tweet_stream(), mimetype="text/event-stream")


@app.route("/hashtags", methods=["GET", "POST"])
def getHashtags():
    if request.method == "GET":
        response = {"hashtags": hashtags}
        return response
    elif request.method == "POST":
        new_hashtag = request.form["hashtags"]
        hashtags.append(new_hashtag)
        print(new_hashtag)
        return "success"




if __name__ == '__main__':
    # create a new socket and connect to it
    
    app.run(threaded=True)