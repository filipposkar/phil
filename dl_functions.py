# -*- coding: utf-8 -*-
"""dl_functions.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FmN7Wi69iDxDX9W-yu4J80rXwGCgsEnH
"""

# deep parse functions
import numpy as np

# Convert address to NGRAM
def convert_word_to_ngram(word, ngram):
  """
  converts a word to ngrams
  """
  import numpy as np
  
  word_list = []

  word_chars = list(word)
  word_len = len(word_chars)

  for i in np.arange(1, word_len, 1):
    word_list.append(word_chars[i-1])
    if i % ngram == 0:
      word_list.append(" ")
  word_list.append(word_chars[word_len-1])

  return "".join((x) for x in word_list)

# Make function to split sentences into characters
def split_chars(text):
  return(" ".join(list(text)))

# Strip accents and lowercase
import unicodedata

def strip_accents_and_lowercase(s):
   return ''.join(c for c in unicodedata.normalize('NFD', str(s))
                  if unicodedata.category(c) != 'Mn').lower()

def convert_address_to_model_input_2(address, model_name):

  """
  convert address to model input
  ---------------------------------
  The address is given as is (text).
  The address is standarized by the function code using the strip_accents_and_lowercase function.
  """

  import tensorflow as tf
  import unicodedata

  address_standarize = strip_accents_and_lowercase(address)
  address_split = address_standarize.split()
  address_char = []
  for element in address_split:
    address_char.append(split_chars(element))
  address_ngram = []
  for element in address_split:
    address_ngram.append(convert_word_to_ngram(element,3))

  if model_name == "model_0": # baseline model (OK)
    converted_address = address_split

  if model_name == "model_100" or model_name == "model_1": # conv1d (OK)
    converted_address = tf.constant(address_split)

  if model_name == "model_200" or model_name == "model_2": # conv1d_positional_embeddings (OK)

    address_length = len(address_split)

    # create line_numbers one hot
    line_numbers_indices = tf.range(0, address_length, 1)
    line_numbers_depth = 10
    line_numbers = tf.one_hot(line_numbers_indices, line_numbers_depth)

    # create total_lines one hot {8/7/2024}
    if address_length > 1:
      total_lines_indices = tf.fill([1, address_length], address_length-1)
      total_lines_depth = 10
      total_lines = tf.one_hot(total_lines_indices, total_lines_depth)
      total_lines = tf.squeeze(total_lines)
    else:
      total_lines_indices = tf.fill([1, address_length], address_length)
      total_lines_depth = 10
      total_lines = tf.one_hot(total_lines_indices, total_lines_depth)
      total_lines =tf.reshape(total_lines, [1, total_lines_depth])

    # create formated address
    converted_address = (line_numbers,
        total_lines,
        tf.constant(address_split))

  if model_name == "model_300" or model_name == "model_3": # conv1d_ngram_embeddings (OK)
    converted_address = tf.constant(address_ngram)

  if model_name == "model_300a" or model_name == "model_3a": # conv1d_ngram_embeddings (OK)
    converted_address = tf.constant(address_char)

  if model_name == "model_400" or model_name == "model_4": # bilstm_ngram_embeddings (OK)
    converted_address = tf.constant(address_ngram)

  if model_name == "model_500": # token_conv1d_and_bilstm_ngram_embeddings (OK)
    converted_address = (tf.constant(address_split), tf.constant(address_ngram))

  if model_name == "model_600" or model_name == "model_6": # token_char_and_pos_embeddings (OK)
    address_length = len(address_split)

    line_numbers_indices = tf.range(0, address_length, 1)
    line_numbers_depth = 10
    line_numbers = tf.one_hot(line_numbers_indices, line_numbers_depth)
    line_numbers

    # create total_lines one hot {8/7/2024}
    if address_length > 1:
      total_lines_indices = tf.fill([1, address_length], address_length-1)
      total_lines_depth = 10
      total_lines = tf.one_hot(total_lines_indices, total_lines_depth)
      total_lines = tf.squeeze(total_lines)
    else:
      total_lines_indices = tf.fill([1, address_length], address_length)
      total_lines_depth = 10
      total_lines = tf.one_hot(total_lines_indices, total_lines_depth)
      total_lines =tf.reshape(total_lines, [1, total_lines_depth])

    # create formated address
    converted_address = (line_numbers,
		total_lines,
		tf.constant(address_split),
		tf.constant(address_char))

  return converted_address

def display_pred_probs_text(text, pred_probs, class_names):
  """
  parameters:
   * text:        an address list of format like: 'Πετρούπολη'
   * pred_probs:  a pred_probs array of shape (address list lenght, number of class_names)
   * class_names: list of class_names

  returns:
   * text & pred_text as string

  call: display_pred_probs('Πετρούπολη', model_0.predict_proba([strip_accents_and_lowercase('Πετρούπολη')]))
  """

  pred_index = pred_probs.argmax()
  pred_text = class_names[pred_index]
  pred_probability = pred_probs[0][pred_index]*100

  # print(f"{text} ===> {pred_text} ({pred_probability:.1f}%)")

  pred_text = class_names[pred_index]

  return text, pred_text, pred_probability

def display_pred_probs_list(class_names,
                         address_split,
                         pred_probs,
                         score = 0,
                         print_out = True):

  """
  example of input (address_split)
  address_split = ['λαογραφικου', 'μουσειου', '34,', 'πυλαια,', '55535']
  address_split = ['αγγ.γεροντα', '1', 'πλακα']

  returns a dictionary
  the label of every token of the address
  and the label score
  """

  # class_names

  # create and initialize pred_dict
  pred_dict = {}
  for idx, i in enumerate(class_names):
    # print(idx, i)
    # pred_dict[i] = None
    pred_dict[i] = ""

  # for key, value in pred_dict.items():
  #   print(key, value)


  for i in np.arange(0, len(pred_probs), 1):

    addr_field = address_split[i].replace(" ","") # splitted address field
    pred_prob_argmax = pred_probs[i].argmax() # prediction index of max probability
    pred_field = class_names[pred_prob_argmax] # class name
    pred_prob = round(pred_probs[i][pred_prob_argmax] * 100, 2) # prediction probability

    if pred_prob > score:
      if print_out:
        print(pred_field, addr_field, pred_prob)
      pred_dict[pred_field] = str(pred_dict.get(pred_field)) + ' ' + addr_field
      pred_dict[pred_field+'_score'] = str(pred_dict.get(pred_field+'_score')) + ' ' + str(pred_prob)

  return pred_dict

def reorder_and_join(streetNames, streetNumbers, reordered_address):

  # streetNames = ["Μελισίων", "Μουργκάνας", "Μαρούσι"]
  # streetNumbers = ["&", "18", "1"]
  
  import re
  try:
    combined_list = streetNames + streetNumbers

    sorted_elements = []

    for word in re.split(r"(\s+)", reordered_address):
      word = word.strip()
      if word in combined_list:
        sorted_elements.append(word)
        combined_list.remove(word)

    return " ".join(sorted_elements)
  except Exception as error:
    print(error)

def terra_geocoding_service(addr):

  """
  input : 'Καραϊσκάκη 32, 26221, Πάτρα'
  
  output :
  [{'addType': 1,
  'addId': 263219,
  'addZip': '26221',
  'addStreet': 'Καραϊσκάκη Γεωργίου ',
  'addMunicip': 'Πάτρα',
  'addNumb': 32,
  'addPoint': {'x': 302124.0, 'y': 4235460.0},
  'addPointWGS84': None,
  'addFormated': 'Καραϊσκάκη Γεωργίου  32 &lt;b&gt;Πάτρα&lt;/b&gt; 26221'}]
  """
  

  
  import os
  import requests
  import json

  data={}
  url = "http://mapsrv9.terra.gr/avl/webservice.asmx/getAddressJSON"


  addr = addr.replace('&', '%26')

  data['countryCode'] = '30'
  data['input'] = addr
  data['SRID'] = '2100'

  query_string = ''
  for k, v in data.items():
      query_string += k + '=' + v + '&'

  url = url + '?'+ query_string[:-1]
  # print(url)

  session = requests.Session()
  session.stream = True
  resp = session.get(url=url)

  address_list = json.loads(resp.text[76:-9])

  return address_list




