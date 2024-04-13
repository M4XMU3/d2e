import sys
import re

translation=('' + sys.argv[2])
file_path=('' + str(sys.argv[4]) + '_lix_scores.csv')

# calculate metrics
def calculate_lix(text):
    # Remove punctuation and split the text into words
    words = re.findall(r'\b\w+\b', text, flags=re.U)  # Use re.U for Unicode support

    # Count the number of words, sentences, and long words
    num_words = len(words)
    num_words = max(num_words, 1)
    # set num_sentences to 1 if 0, so we do not divide through 0!
    num_sentences = text.count('.') + text.count('!') + text.count('?')
    num_sentences = max(num_sentences, 1)
    num_long_words = sum(1 for word in words if len(word) > 6)

    # Calculate LIX
    lix = (num_words / num_sentences) + (num_long_words * 100 / num_words)

    return lix

lix_score = str(calculate_lix(translation)).replace('.', ',')

print(translation)
print('LIX: ' + str(lix_score))
print('------')

if lix_score:
    with open(file_path, 'a') as file:
        print(f"{lix_score}", file=file)
else:
        print('error in calculating score', file=file)


import re