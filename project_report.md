# Project report
> Mark-Eerik Kodar, Aleksander Parelo

Our project aimed to make use of the SparkML and Spark Streaming applications to create a visual dashboard for displaying tweet sentiments based on hashtags on a world map.

Link to the final solution: http://64.225.110.173/

## Implementation

### Tweet sentiment classification

As the process of streaming tweets by yourself and then labeling them by hand would be extremely time consuming, then we opted for using an open-source training dataset which had labeled tweets to three classes: positive, negative and neutral. 

We opted for using SparkML to implement the preprocessing and classification of tweets.
As the training dataset had not been preprocessed, then we needed to apply some preprocessing steps. The steps included tokenization, stop words removal, removing links, emoticons, special symbols and etc. After that we created bigrams of these filtered tweets and then applied TF-IDF. As the SparkML NaiveBayesModel requires that the input data to be in the form of a LabeledPoint, where the second argument is a sparse vector, then we needed to apply this conversion as well.

After training we saw that our model had test set accuracy of 47.3%, which is much better than random, but could still be a lot better. But unfortunately, we did not have time to improve upon our model. We then proceeded to save our model to be used in the final application.

### Streaming tweets

The tweets are streamed from Twitter using the Tweepy library. To stream tweets from Twitter a list of keywords or hashtags needs to be provided, Twitter will then return a stream of Tweets matching these hashtags. Unfortunately it is not possible to specify that only tweets with locations should be returned by the API, this means that the application has to manually check each tweet for location data and discard the Tweets that do not contain any location data.

During development of the application it was noticed that only a very small fraction of tweets had location data so it was decided to add dummy locations to tweets that did not contain any location data. This was done by adding random coordinates to tweets that do not have location data.

Then our twitter stream is sent to our Spark engine over a socket connection. The Spark Streaming Context is listening on that socket and preprocesses them before predicting the sentiment of the tweet using our pre-loaded Naive Bayes Model.


### Displaying sentiment

After the tweets have been labeled by Spark they are sent to a web server using a POST request. The web server then sends the tweets to the client using the Javascript eventsource API. Eventsource API allows the client to receive the tweets in real time as they arrive at the web server. Eventsource API was chosen for this because it is a native Javascript API that is supported by most modern browsers without any external libraries. 

### Visualization
To visualize the Tweets HERE maps API was used, we chose the HERE maps API since it is free to use and provides all the features we need for this project. The API is also very easy to use and implement. The Javascript API from HERE maps was used to display a map for the user and to add markers to the map that correspond to Tweet locations. These markers are made up of SVG assets thta can be easily modified to represent different sentiments of the tweets. 

### Deployment

The project is deployed on a DigitalOcean server that is running Ubuntu. The application is run by turning the different scripts into Linux services. This was done to allow all the different services to run concurrently. Spark job was submitted using spark-submit and using flags that allow the Spark job to continue running on the Spark cluster after client disconnect.
### Solution Evaluation

I think if we had more time then we could have developed a better model or at least have tried some other pretrained models, as the sentiment accuracy was quite low. Another thing that we would have liked to have done better would be the visualization of tweets as there was some lag between the client receiving tweets and the client showing them, but we could not figure out why this was happening. What is more, then we currently do not retrain our model with incoming tweets and this can be improved by using Apache Airflow. 

Regarding Spark, then an additional improvement could be by batching tweets using bigger windows, as we saw that the amount of tweets that come using this use case is relatively small, then when we would have tweets coming at a greater intensity then it would be more beneficial to group them using bigger windows. Currently the tweets are read from the socket text stream in a 1 second interval and directly processed.

Another point of improvement would be to Dockerize the application as we faced significant issues in managing the different Python and Java versions in the remote server. Docker would eliminate such issues by default.

we could also improve the user experience of the client application as it is currently quite basic and lacks some features. For example the option to remove hashtags could be added and the design of the client could also be improved.
