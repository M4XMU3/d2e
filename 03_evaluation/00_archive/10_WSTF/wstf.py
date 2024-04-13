import sys
#import textstat

test_data=('' + sys.argv[1])
file_path=('' + str(sys.argv[2]) + '_wstf_scores.csv')

def wiener_sachtextformel(text):
    # Assume that text is a string containing the input text

    # Count the number of words in the text
    words = text.split()
    num_words = len(words)

    # Count the number of sentences in the text
    sentences = text.split('.')
    num_sentences = len(sentences)

    # Calculate the average sentence length (SL)
    average_sentence_length = num_words / num_sentences

    # Calculate the percentage of words with three or more syllables (MS)
    num_syllables = sum([sum([1 for char in word if char.lower() in 'aeiouy']) for word in words])
    percentage_more_syllables = sum([1 for word in words if sum([1 for char in word if char.lower() in 'aeiouy']) >= 3]) / num_words

    # Calculate WSTF4 score
    wstf_score = 0.2565 * average_sentence_length + 0.2744 * percentage_more_syllables - 1.693

    return wstf_score

# Example usage
wstf_score = str(wiener_sachtextformel(test_data)).replace('.', ',')

print(test_data)
print('WSTF: ' + wstf_score)

if wstf_score:
    with open(file_path, 'a') as file:
        print(f"{wstf_score}", file=file)
else:
        print('error in calculating score', file=file)
