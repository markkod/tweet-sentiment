import tweepy
import socket
import json
import random
from ast import literal_eval
from flask import Flask, render_template, request, Response, send_from_directory
from config import consumer_key, consumer_secret, access_token, access_token_secret


hashtags = ["#sunset", "#horse", "#dogsofinstagram", "#travel", "#location", "#party", "#event", "#like"]

TCP_IP = "localhost"
TCP_PORT = 9009

app = Flask(__name__)
# app.debug = True

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, conn):
        self.connection = conn
        
    def on_data(self, data):
        fakeLocation = True # add dummy location to tweets without location
        status = json.loads(data)
        if(status is not None):
            if(status["coordinates"] is not None) or (fakeLocation is True):
                if(status["coordinates"] is None):
                    lat = random.randint(-90, 90)
                    lon = random.randint(-180, 180)
                    status["coordinates"] = dict()
                    status["coordinates"]["coordinates"] = [lon, lat]
                print(status["text"])
                print(status["coordinates"])
                myobj = {'text': status["text"], 'loc':', '.join(str(x) for x in status["coordinates"]['coordinates'])}

                try:
                    self.connection.sendall((json.dumps(myobj)+ "\n").encode('utf-8'))
                except:
                    print("Error sending data")
                    return False

conn = None
myStream = None

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)




        



    


@app.route("/addhashtags", methods=["POST"])
def addHashtags():
    global hashtags
    myStream.disconnect()
    hashtags = request.json["hashtags"]
    print(hashtags)
    myStream.filter(track=hashtags, languages=["en"], is_async=True)
    return "good"
    



def start_socket(TCP_IP, TCP_PORT):
    global myStream
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(5)


    print("Waiting for TCP connection...")
    conn, addr = s.accept()
    print("Connected... Starting getting tweets.")

    print(hashtags)
    myStream = tweepy.Stream(api.auth, MyStreamListener(conn))
    myStream.filter(track=hashtags, languages=['en'], is_async=True)




if __name__ == '__main__':

    start_socket(TCP_IP, TCP_PORT)

    app.run()

# s.close()


