#import sys
#test_data=str(sys.argv[1])
#file_path=str(sys.argv[2]) + '_sentence_scores.csv'
#
#def count_newlines_and_sentences(text):
#    newline_count = text.count('\n')
#    sentence_count = text.count('.') + text.count('!') + text.count('?')
#    colon_count = text.count(',')
#    if sentence_count == 0:
#        sentence_count = newline_count
#    nsr = round(newline_count / sentence_count, 2)
#    return newline_count, sentence_count, colon_count, nsr
#
#newline_count, sentence_count, colon_count, nsr = count_newlines_and_sentences(test_data)
#
#print('------')
#print(test_data)
#print("newlines:", newline_count)
#print("sentences:", sentence_count)
#print("nsr:", nsr)
#print("colons:", colon_count)
#
#if sentence_count:
#    with open(file_path, 'a') as file:
#        print(f"{newline_count};{sentence_count};{nsr};{colon_count}", file=file)
#else:
#        print('error in calculating score', file=file)
#

import sys
import spacy
import re

# Load SpaCy German model
# Ensure that the SpaCy model is installed
try:
    nlp = spacy.load("de_core_news_sm")
except OSError:
    print("SpaCy German model 'de_core_news_sm' not found. Please run 'python -m spacy download de_core_news_sm' to install it.")
    sys.exit(1)

# Get input from command line arguments
test_data = str(sys.argv[1])
file_path = str(sys.argv[2]) + '_sentence_scores.csv'

# Function to count newlines, sentences, colons, and calculate nsr
def count_newlines_and_sentences(text):
    # Use splitlines to get a list of lines, then count the elements
    ## newline + 1 so that a single row also counts as one line; otherweise nsr is not correct
    newline_count = text.count('\\n') + 1

    # Split the text by common sentence-ending punctuation marks
    sentences = [sentence.strip() for sentence in re.split(r'[.!?]', text) if sentence.strip()]
    # Use SpaCy for sentence tokenization
    doc = nlp(text)
    sentence_count = len(sentences)
#    sentence_count = len(list(doc.sents))

    # Count colons in the text
    colon_count = text.count(',')

    # Calculate nsr (newline-to-sentence-ratio)
    nsr = round(newline_count / max(1, sentence_count or newline_count), 2)  # Avoid division by zero

    return newline_count, sentence_count, colon_count, nsr

# Call the function to get counts and ratios
newline_count, sentence_count, colon_count, nsr = count_newlines_and_sentences(test_data)

# Print the results to the console
print('------')
print(test_data)
print("newlines:", newline_count)
print("sentences:", sentence_count)
print("nsr:", nsr)
print("colons:", colon_count)

# Write the results to a file
if sentence_count:
    with open(file_path, 'a') as file:
        print(f"{newline_count};{sentence_count};{nsr};{colon_count}", file=file)
else:
    print('error in calculating score', file=sys.stderr)

