import sys

from pyspark import SparkConf, SparkContext
from pyspark.sql import Row, SQLContext
from pyspark.streaming import StreamingContext
from pyspark.mllib.classification import NaiveBayes, NaiveBayesModel
import os
import json
import pandas as pd

from utils import preprocess_row_df


def get_sql_context_instance(spark_context):
    if 'sqlContextSingletonInstance' not in globals():
        globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
    return globals()['sqlContextSingletonInstance']


def predict_sentiment(time, rdd):
    print("----------- %s -----------" % str(time))
    try:
        if not rdd.isEmpty():
            # Get spark sql singleton context from the current context
            sql_context = get_sql_context_instance(rdd.context)
            
            tweet_info = json.loads(str(rdd.collect()[0]))
            df = pd.DataFrame.from_records([tweet_info])
            df.columns = ['sentence', 'coordinates']
            sdf = sql_context.createDataFrame(df)
            sdf.show()
            preprocessed_df = preprocess_row_df(sdf)
            model.predict(preprocessed_df).collect()
    except:
        e = sys.exc_info()
        print("Error: %s" % str(e))


conf = SparkConf('local')
conf.setAppName("TwitterSentiment")
sc = SparkContext(conf=conf)
sc.setLogLevel('ERROR')

ssc = StreamingContext(sc, 5)
ssc.checkpoint('checkpoint_TwitterSentiment')
data_stream = ssc.socketTextStream('localhost', 9009)

data_stream.foreachRDD(predict_sentiment)

model_path = os.path.join(os.getcwd(), "model") 
print(model_path)
model = NaiveBayesModel.load(sc, model_path)

ssc.start()
# wait for the streaming to finish
ssc.awaitTermination()
