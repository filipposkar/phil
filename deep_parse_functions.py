

def convert_word_to_ngram(word, ngram):
  """
  converts a word to ngrams
  """
  word_list = []

  word_chars = list(word)
  word_len = len(word_chars)

  for i in np.arange(1, word_len, 1):
    word_list.append(word_chars[i-1])
    if i % ngram == 0:
      word_list.append(" ")
  word_list.append(word_chars[word_len-1])

  return "".join((x) for x in word_list)