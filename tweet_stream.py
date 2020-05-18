import tweepy
import socket
import json
from config import consumer_key, consumer_secret, access_token, access_token_secret

hashtags = ["#sunset", "#horse", "#dogsofinstagram"]

TCP_IP = "localhost"
TCP_PORT = 9009
conn = None

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, conn):
        self.connection = conn
        
    def on_data(self, data):
        status = json.loads(data)
        if(status["coordinates"] is not None):
            print(status["text"])
            print(status["coordinates"])
            myobj = {'text': status["text"], 'loc':status["coordinates"]}
            try:
                self.connection.send(json.dumps(myobj).encode('utf-8'))
            except:
                print("Error sending data")





s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Waiting for TCP connection...")
conn, addr = s.accept()
print("Connected... Starting getting tweets.")

myStream = tweepy.Stream(api.auth, MyStreamListener(conn))
myStream.filter(track=hashtags)