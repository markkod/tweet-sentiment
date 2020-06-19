# tweet-sentiment
Visualize hashtag based tweet sentiment using SparkML, Spark Streaming, Python.

Requirements:
- Python 3.6
- Apache Spark (requires Java 8, Scala 11)

To run locally:
```
git clone https://github.com/markkod/tweet-sentiment
cd tweet-sentiment
pip install -r requirements.txt
```

NB! Make sure that the pyspark python version is less 3.6 or 3.7 and Spark uses Java 8.

Open three terminal windows and run each of the following commands in a separate window.
```
python tweet_stream.py
python socket_client.py
spark-submit spark_engine.py
```

The application will be served at: http://127.0.0.1:5001