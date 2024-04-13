import sys
import re
from nltk.tokenize import sent_tokenize


text="" + sys.argv[2]
file_path=str(sys.argv[4]) + '_snlr_scores.csv'


def sentence_new_line_ratio(text):
    sentences = sent_tokenize(text)
    num_sentences = len(sentences)
    # Considering text ending as a new line => + 1
    num_new_lines = len(re.findall('\n', text)) + 1 
    
    # To prevent Division by Zero
    if num_sentences == 0:
        snl_ratio = 0
    else:
        # Adding max bound as 1, if text ending has newline or text has several newlines for formatting reasons
        snl_ratio = min(num_new_lines/num_sentences, 1.0)
    return snl_ratio

# Testing the function on a sample text
# text = "Hello, my name is AI.\nI'm here to help you. \nHow can I assist?\n\n\n\nLet's write good code!\nsheesh\n\n\n\n"
# calculate snl_ratio for given text
snl_ratio = sentence_new_line_ratio(text)
print("------\nsentence/new-line ratio: ", snl_ratio)


if snl_ratio:
   with open(file_path, 'a') as file:
       print(str(snl_ratio).replace('.', ','), file=file)
else:
       print('error in calculating sari score', file=file)
