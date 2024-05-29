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

# Standarize address 1
# Strip accents and lowercase
import unicodedata

def strip_accents_and_lowercase(s):
   return ''.join(c for c in unicodedata.normalize('NFD', str(s))
                  if unicodedata.category(c) != 'Mn').lower()


# Make function to split sentences into characters
def split_chars(text):
  return(" ".join(list(text)))

# Convert address to model input
def convert_address_to_model_input(address, 
                                   standarize_bool=False, 
                                   ngram_bool=False,
                                   line_order_bool=False,
                                   token_and_ngram_bool=False,
                                   char_bool=False):
  """
  input: address string and converts it to model input format for prediction
  output: convered address
  parameters: model_name
  """

  """
  accepts as input an address string and converts it to model input format for prediction
  """

  import unicodedata

  if standarize_bool:
    address = strip_accents_and_lowercase(address) 

  # models: baseline, conv1d
  # "model_0", "model_1", "model_100"
  formated_address_conv1d = address.split()
  formated_address = formated_address_conv1d

  # models: ngram
  if ngram_bool:
    formated_address_list_ngram = []
    for addr_element in address.split():
      formated_address_list_ngram.append(convert_word_to_ngram(addr_element,3))
    formated_address = formated_address_list_ngram

  # models: char embed
  if char_bool:
    formated_address_list_char = []
    for element in formated_address:
      formated_address_list_char.append(split_chars(element))
    formated_address = formated_address_list_char
  
  # models: "model_conv1d_line_order"
  # "model_300"
  if line_order_bool:
    import tensorflow as tf
    address_length = len(formated_address)

    # create line_numbers one hot
    line_numbers_indices = tf.range(0, address_length, 1)
    line_numbers_depth = 10
    line_numbers = tf.one_hot(line_numbers_indices, line_numbers_depth)

    # create total_lines one hot
    total_lines_indices = tf.fill([1, address_length], address_length-1)
    total_lines_depth = 10
    total_lines = tf.one_hot(total_lines_indices, total_lines_depth)
    total_lines = tf.squeeze(total_lines)

    # create formated address
    formated_address = (line_numbers,
        total_lines,
        tf.constant(formated_address))
    
  if token_and_ngram_bool:
    import tensorflow as tf
    formated_address = (tf.constant(formated_address_conv1d), tf.constant(formated_address_list_ngram))
    
  return formated_address

def terra_geocode(addr):
  import os
  import requests
  import json

  url = "http://mapsrv5.terra.gr/avl/webservice.asmx/getAddressJSON"

  data={}
  # data['code'] = 'Age78em3xSOpTGLSV+Ukks5Jk+q87IKsYX6WLpKhWdfiN6cldyr2y5WS66HTwtlam5mmXA7RdFCBFJGyGgXSV4WncMeoekitmyyDeRinO10P2KK0TEWJOJAZfVgPZ69t/igyp7s0un2EA1e1TlrpfPCo8JBJbliuuqUmnHZIqDWW6HkRpe6mJhUbiPBhQLqSpRvKgEmBa1WOjJ+/uZdgNw=='
  # data['machineID'] = 'XLS-4F1C8ECF-9EA2-45DA-A349-B6E06AEE3A2F'
  data['countryCode'] = '30'
  data['input'] = address_text
  data['SRID'] = '2100'

  query_string = ''
  for k, v in data.items():
      query_string += k + '=' + v + '&'

  url = url + '?'+ query_string[:-1]

  session = requests.Session()
  session.stream = True
  resp = session.get(url=url)

  address_list = json.loads(resp.text[76:-9])

  return address_list

