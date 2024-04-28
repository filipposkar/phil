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
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn').lower()


# Make function to split sentences into characters
def split_chars(text):
  return(" ".join(list(text)))

# Convert address to model input
def convert_address_to_model_input(address, 
                                   standarize_bool=False, 
                                   ngram_bool=False, 
                                   char_bool=False):
  """
  accepts as input an address string and converts it to model input format for prediction
  it is better to replace char_embed_bool to model name (model_1, etc.)
  """

  import unicodedata

  if standarize_bool:
    address = strip_accents_and_lowercase(address)

  # models: baseline, conv1d
  formated_address = address.split()

  # models: ngram
  if ngram_bool:
    formated_address = convert_word_to_ngram(address, 3)

  # models: char embed
  if char_bool:
    formated_address_list = []
    for element in formated_address:
      formated_address_list.append(split_chars(element))
    formated_address = formated_address_list

  return formated_address

