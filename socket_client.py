import socket
from queue import Queue
from flask import Flask, render_template, request, Response, send_from_directory
from pyspark.sql import SparkSession, SQLContext


app = Flask(__name__, static_url_path="", static_folder='static')
app.debug = True


# get the spark app for reading data
spark = SparkSession.builder.appName("TwitterSentiment").getOrCreate()

dataFrame = SQLContext(spark)




def tweet_stream():
    print("Stream started")
    print(hashtags)
    while True:
        print("Test")


@app.route('/')
def hello():
    return render_template('dashboard.html')

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('templates', path)



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
        print(hashtags)
        return "success"




if __name__ == '__main__':
    # create a new socket and connect to it
    
    app.run(threaded=True)