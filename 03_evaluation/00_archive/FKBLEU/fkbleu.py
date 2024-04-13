import sys
import nltk
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction
import spacy
from math import exp

# Load the spaCy German language model
nlp = spacy.load("de_core_news_md")

# Function to calculate BLEU score
def calculate_bleu(candidate, reference):
    candidate_tokens = candidate.split()
    reference_tokens = [reference.split()]
    smoothing = SmoothingFunction().method1
    return sentence_bleu(reference_tokens, candidate_tokens, smoothing_function=smoothing)

# Function to calculate FK score
def calculate_fk(sentence):
    doc = nlp(sentence)
    num_words = max(1, len(doc))
    num_sentences = max(1, len(list(doc.sents)))
    num_syllables = sum([len(token.text) / 2 for token in doc if not token.is_punct])
    return 0.39 * (num_words / num_sentences) + 11.8 * (num_syllables / num_words) - 15.59

# Function to calculate FKBLEU score
def calculate_fkbleu(candidate, reference, input_text, alpha=0.9):
    # Calculate iBLEU
    bleu_reference = calculate_bleu(candidate, reference)
    bleu_input = calculate_bleu(candidate, input_text)
    ibleu = alpha * bleu_reference - (1 - alpha) * bleu_input
    
    # Calculate FK difference
    fk_candidate = calculate_fk(candidate)
    fk_input = calculate_fk(input_text)
    fk_diff = sigmoid(fk_candidate - fk_input)
    
    # Calculate FKBLEU
    fkbleu = ibleu * fk_diff
    return fkbleu

# Sigmoid function
def sigmoid(x):
    return 1 / (1 + exp(-x))

# Example usage
# candidate_summary = "Die Katze sitzt auf der Matte."
# reference_summary = "Die Katze ist auf der Matte."
# input_text = "Die Katze sitzt auf der Matte, während die Sonne scheint."
alpha = 0.9
# get input_text from command line arguments
to_translate = str(sys.argv[1])
translation = str(sys.argv[2])
reference_translation = str(sys.argv[3])
file_path = str(sys.argv[4]) + '_fkbleu_scores.csv'

fkbleu_score = calculate_fkbleu(translation, reference_translation, to_translate, alpha)
print(fkbleu_score)
if fkbleu_score:
    print(f'text: {to_translate}\nscore: {fkbleu_score}\n------')
    with open(file_path, 'a') as file:
        print(str(fkbleu_score).replace('.', ','), file=file)
else:
    print('error')
    with open(file_path, 'a') as file:
        print('error in score', file=file)
