import math
import json
from IPython import display
from matplotlib import cm
from matplotlib import gridspec
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn import metrics
import tensorflow as tf
from tensorflow.python.data import Dataset
import re
from collections import Counter
import io


tf.logging.set_verbosity(tf.logging.ERROR)
pd.set_option('display.max_columns', 500)
pd.options.display.float_format = '{:.1f}'.format

NUM_OF_WORDS = 30
word_list = []
word_is_there = False

with io.open('outputfile.json', 'r', encoding='UTF-8-sig') as f: # open up the file
    rap_lyrics_data = json.load(f) # load it into a json format

for rapper in range(len(rap_lyrics_data)):
    
    rap_lyrics_data [rapper]["coordinates"] = rap_lyrics_data[rapper]["coordinates"].split(',')
    rap_lyrics_data[rapper].update({'longitude' : rap_lyrics_data[rapper]["coordinates"][0]})
    rap_lyrics_data[rapper].update({'latitude' : rap_lyrics_data[rapper]["coordinates"][1]})
    rap_lyrics_data[rapper].pop('coordinates')
    #convert the coordinates data into latitude and longitude
    words = re.findall(r'\w+', rap_lyrics_data[rapper]['lyrics'])
    cap_words = [word.upper() for word in words]
    word_counter = Counter(cap_words)
    most_common = word_counter.most_common(NUM_OF_WORDS)
    for word in range(len(most_common)):
    	if most_common[word][0] in word_list:
    		pass
    	else:
    		word_list.append(most_common[word][0])
    
    one_hot_encoding = [] # encoding to store whether a word is in the rapper's most common vocab
    
    for word in range(len(word_list)):
        word_is_there = False
        for word2 in range(len(most_common)):
            if word_list[word] == most_common[word2][0]:
   	            word_is_there = True
            else:
                pass
        if word_is_there:
            one_hot_encoding.append(1)
        else:
    	    one_hot_encoding.append(0)
    rap_lyrics_data[rapper].update({'word_frequency' : one_hot_encoding})
full_length = len(rap_lyrics_data[-1]['word_frequency'])

for rapper in range(len(rap_lyrics_data)):
	while len(rap_lyrics_data[rapper]['word_frequency']) < full_length:
		rap_lyrics_data[rapper]['word_frequency'].append(0)

rap_lyrics_dataframe = pd.DataFrame(rap_lyrics_data)

  	

rap_lyrics_dataframe = rap_lyrics_dataframe.reindex(
    np.random.permutation(rap_lyrics_dataframe.index))


def preprocess_features(rap_lyrics_dataframe):
    """Prepares input features from rap lyrics dataset.

  Args:
    rap_lyrics_dataframe: A Pandas DataFrame expected to contain data
      from the rap_lyrics data set.
  Returns:
    A DataFrame that contains the features to be used for the model, including
    synthetic features.
  """
    selected_features = rap_lyrics_dataframe[["word_frequency"]]
    return(selected_features)

def preprocess_targets(rap_lyrics_dataframe):
    """Prepares target features (i.e., labels) from rap lyrics data set.

  Args:
    rap_lyrics_dataframe: A Pandas DataFrame expected to contain data
      from the rap_lyrics data set.
  Returns:
    A DataFrame that contains the target features.
  """
    output_targets = pd.DataFrame()
  # Scale the target to be in units of thousands of dollars.
    output_targets["longitude"] = (
        rap_lyrics_dataframe["longitude"])
    output_targets["latitude"] = (
  	    rap_lyrics_dataframe["latitude"])
    return(output_targets)

training_examples = preprocess_features(rap_lyrics_dataframe.head(20))

validation_examples = preprocess_features(rap_lyrics_dataframe.tail(8))

training_targets = preprocess_targets(rap_lyrics_dataframe.head(20))

validation_targets = preprocess_targets(rap_lyrics_dataframe.tail(8))
