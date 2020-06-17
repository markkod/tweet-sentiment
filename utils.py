import re
import string
from pyspark.ml.feature import Tokenizer, StopWordsRemover, NGram, HashingTF, IDF
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType, IntegerType
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.linalg import Vectors

"""
This file contains all of the necessary functions for processing DFs that can eventually
be used by the model to predict the sentiment of the tweets.
"""

pattern = re.compile(r'[\d|)(:\(|:\))+$]')

def is_unwanted_word(word):
    if '@' in word:
        return True
    elif '#' in word:
        return True
    elif 'http://' in word:
        return True
    elif 'https://' in word:
        return True
    elif word == 'RT':
        return True
    elif pattern.match(word):
        return True
    return False


def remove_punctuation(word):
    return word.translate(str.maketrans('', '', string.punctuation))


def remove_unwanted_values(values):
    return [remove_punctuation(x) for x in values if not is_unwanted_word(x)]


def tokenize(row_df):
    tokenizer = Tokenizer(inputCol='sentence', outputCol='tokenized')
    return tokenizer.transform(row_df)


def remove_stop_words(row_df):
    remover = StopWordsRemover(inputCol='tokenized', outputCol='stopwords')
    return remover.transform(row_df)


def remove_special_characters(row_df):
    map_udf = udf(remove_unwanted_values, ArrayType(StringType()))
    return row_df.withColumn('filtered', map_udf(row_df.stopwords))

def create_bigrams(row_df):
    ngram = NGram(n=2, inputCol='filtered', outputCol='bigrams')
    return ngram.transform(row_df)

def tfidf(row_df):
    hashingTF = HashingTF(inputCol='bigrams', outputCol='TF', numFeatures=20000)
    tf_df = hashingTF.transform(row_df)

    idf = IDF(inputCol='TF', outputCol='TF-IDF')
    idfModel = idf.fit(tf_df)
    idf_df = idfModel.transform(tf_df)

    # Convert labels to sparse vectors, that are needed by the classifer
    coordinates = tf_df.select("coordinates").rdd.flatMap(lambda x: x).collect()
    return coordinates, tf_df.rdd.map(lambda row: LabeledPoint(0.0, Vectors.fromML(row.TF)))



def preprocess_row_df(row_df):
    row_df = tokenize(row_df)
    row_df = remove_stop_words(row_df)
    row_df = remove_special_characters(row_df)
    row_df = create_bigrams(row_df)
    return tfidf(row_df)


