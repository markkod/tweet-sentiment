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

The tweets are streamed from Twitter using the Tweepy library. The initial idea was to stream only tweets that have location coordinates attached to them, but soon we noticed that there are so few tweets that have location attached to them, so we streamed tweets without locations as well, but added a dummy location to them. 

Then our twitter stream is sent to our Spark engine over a socket connection. The Spark Streaming Context is listening on that socket and preprocesses them before predicting the sentiment of the tweet using our pre-loaded Naive Bayes Model.


### Displaying sentiment

After the tweets have been given labels, then they are batched and sent to the client that displays the sentiments based on coordinates on a map. These sentiments are not sent over a socket connection, but rather with a simple HTTP POST request. The server uses Javascript eventstream API to send the Tweets to the browser in real time as they arrive. Eventsource API was chosen for this because it is a native Javascript API that is supported by most modern browsers without any external libraries. 

### Visualization
To visualize the Tweets HERE maps API was used, we chose the HERE maps API since it is free to use and provides all the features we need for this project. The API is also very easy to use and implement. The Javascript API from HERE maps was used to display a map for the user and to add markers to the map that correspond to Tweet locations. These markers are made up of SVG assets thta can be easily modified to represent different sentiments of the tweets. 

### Deployment

The project is deployed on a DigitalOcean server. The application is run by creating services that allow for running different scripts. As our application needs three different scripts to be running at the same time, then a service was created for each one of them. 

### Solution Evaluation

I think if we had more time then we could have developed a better model or at least have tried some other pretrained models, as the sentiment accuracy was quite low. Another thing that we would have liked to have done better would be the visualization of tweets as there was some lag between the client receiving tweets and the client showing them, but we could not figure out why this was happening. What is more, then we currently do not retrain our model with incoming tweets and this can be improved by using Apache Airflow. 

Regarding Spark, then an additional improvement could be by batching tweets using bigger windows, as we saw that the amount of tweets that come using this use case is relatively small, then when we would have tweets coming at a greater intensity then it would be more beneficial to group them using bigger windows. Currently the tweets are read from the socket text stream in a 1 second interval and directly processed.

Another point of improvement would be to Dockerize the application as we faced significant issues in managing the different Python and Java versions in the remote server. Docker would eliminate such issues by default. 
