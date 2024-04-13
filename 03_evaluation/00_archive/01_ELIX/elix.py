import re
import sys

def calculate_einfache_lesbarkeitsindex(text):
    # Tokenize the text into sentences using regular expressions
    sentences = re.split(r'[.!?]', text)

    # Calculate average sentence length (ASL)
    total_words = sum(len(sentence.split()) for sentence in sentences)
    average_sentence_length = total_words / len(sentences)

    # Count the percentage of difficult words (words with more than 3 syllables)
    difficult_word_threshold = 3
    difficult_words_count = sum(1 for word in text.split() if len(word) > difficult_word_threshold)

    # Calculate the percentage of difficult words (PDC)
    total_words_in_text = len(text.split())
    percentage_difficult_words = (difficult_words_count / total_words_in_text) * 100

    # Calculate Einfache Lesbarkeitsindex
    einfache_lesbarkeitsindex = 180 - (average_sentence_length + percentage_difficult_words)

    return einfache_lesbarkeitsindex

# usage
text = str(sys.argv[1])
file_path = (str(sys.argv[2]) + '_elix_scores.csv')
result = calculate_einfache_lesbarkeitsindex(text)

if result:
    print(f'text: {text}\nscore: {result}\n------')
    with open(file_path, 'a') as file:
        print(str(result).replace('.', ','), file=file)
else:
        print('error in score', file=file)