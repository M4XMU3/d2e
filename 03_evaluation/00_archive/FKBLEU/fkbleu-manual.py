import sys
import textstat
import math
import nltk
from nltk.translate.bleu_score import corpus_bleu
from nltk.tokenize import word_tokenize
# nltk.download('punkt')

# get input_text from command line arguments
#to_translate = str(sys.argv[1])
#translation = str(sys.argv[2])
#reference_translation = str(sys.argv[3])
#file_path = str(sys.argv[4]) + '_fkbleu_scores.csv'

# Example usage:
to_translate = "Personalausweis"
translation = "sadfgdfsdfasfsdfsag asdf dasf as fasd."
reference_translation = "Personal-Ausweis"
alpha = 0.9

# Set language to German
textstat.set_lang("de_DE")

# define sigmoid function
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def calculate_ibleu_score(candidate, references, input_text, alpha):
    # Tokenize candidate, reference and input sentences
    candidate_tokens = word_tokenize(candidate.lower())
    reference_tokens = [word_tokenize(reference.lower()) for reference in references]
    input_tokens = word_tokenize(input_text.lower())

    # Calculate BLEU scores
    bleu_output = corpus_bleu([reference_tokens], [candidate_tokens])
    bleu_input = corpus_bleu([reference_tokens], [input_tokens])

    # calculate iBLEU
    ibleu_score = (alpha * bleu_output) - ((1 - alpha) * bleu_input)
    return ibleu_score

# define fkbleu calculation
def calculate_fkbleu(input_text, output_text, reference_text):
    # Calculate Flesch Reading Ease using textstat module with German language setting
    flesch_re_input = textstat.flesch_reading_ease(input_text)
    flesch_re_output = textstat.flesch_reading_ease(output_text)
    flesch_re_diff = flesch_re_output - flesch_re_input
    flesch_diff = sigmoid(flesch_re_diff)
    # calculate iBLEU
    ibleu_score = calculate_ibleu_score(output_text, [reference_text], input_text, alpha)

    # Calculate FKBLEU
    fkbleu = ibleu_score * flesch_diff
    return fkbleu

# usage
input_text = str(sys.argv[1])
output_text = str(sys.argv[2])
reference_text = str(sys.argv[3])
file_path = (str(sys.argv[4]) + '_fkbleu_scores.csv')
result = calculate_fkbleu(input_text, output_text, reference_text)

if result:
    print(f'text: {input_text}\nscore: {result}\n------')
    with open(file_path, 'a') as file:
        print(str(result).replace('.', ','), file=file)
else:
        print('error in score', file=file)
