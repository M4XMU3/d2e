import nltk
import pyphen
from nltk import word_tokenize, sent_tokenize

def syllable_count(word):
    dic = pyphen.Pyphen(lang='de_DE')
    return max(1, len(dic.positions(word)) + 1)

def calculate_gunning_fog_index_german(text):
    words = word_tokenize(text, language='german')
    sentences = sent_tokenize(text, language='german')

    complex_words = [word for word in words if syllable_count(word) >= 3]

    fog_index = 0.4 * ((len(words) / len(sentences)) + 100 * (len(complex_words) / len(words)))
    return fog_index

# Example usage:
german_text = "Personalausweis"
gunning_fog_index_german = calculate_gunning_fog_index_german(german_text)
print("Gunning Fog Index (German):", gunning_fog_index_german)

