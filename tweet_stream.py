import tweepy
import socket
import threading
import json
from config import consumer_key, consumer_secret, access_token, access_token_secret

hashtags = ["#sunset", "#horse", "#dogsofinstagram", "#travel", "#location", "#party", "#event", "#like"]

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
                self.connection.sendall(json.dumps(myobj).encode('utf-8'))
            except:
                print("Error sending data")
                return False



def on_new_client(conn, addr):
    myStream = tweepy.Stream(api.auth, MyStreamListener(conn))
    myStream.filter(track=hashtags)



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while True:
    print("Waiting for TCP connection...")
    conn, addr = s.accept()
    print("Connected... Starting getting tweets.")
    x = threading.Thread(target=on_new_client, args=(conn, addr))
    x.start()

s.close()
    