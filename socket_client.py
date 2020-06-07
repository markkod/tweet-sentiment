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
    print(hashtags)
    s = socket.socket()
    s.connect((HOST, PORT))
    # send the hashtag list and start listening
    s.sendall(bytes(str(hashtags), 'utf-8'))
    while True:
        print("Test")
        data = s.recv(1024)
        print('Received', repr(data))
        if(len(data) != 0):
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
    global hashtags
    if request.method == "GET":
        response = {"hashtags": hashtags}
        return response
    elif request.method == "POST":
        hashtags = request.json["hashtags"]
        print(hashtags)
        return "success"




if __name__ == '__main__':
    # create a new socket and connect to it
    
    app.run(threaded=True)