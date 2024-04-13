import sys
from collections import Counter
import math

def nist_score(reference, candidate, n=4):
    ref_ngrams = [tuple(reference[i:i+n]) for i in range(len(reference)-n+1)]
    cand_ngrams = [tuple(candidate[i:i+n]) for i in range(len(candidate)-n+1)]

    ref_counts = Counter(ref_ngrams)
    cand_counts = Counter(cand_ngrams)

    nist_precision = 0.0
    if cand_ngrams:  # Check if cand_ngrams is not empty
        for ng in cand_counts:
            nist_precision += min(cand_counts[ng], ref_counts.get(ng, 0))

        nist_precision /= len(cand_ngrams)

    nist_precision = max(nist_precision, 1e-10)  # Avoid division by zero

    nist_score = math.pow(nist_precision, 1/n)

    return nist_score

# Example reference and candidate texts
# reference = 'Personalausweis urkundlich beantragen'.split()
# candidate = 'Personal-Ausweis bestellen'.split()
# # Calculate NIST score
# nist = nist_score(reference, candidate)
# print("NIST Score:", nist)

# get input_text from command line arguments
to_translate = str(sys.argv[1])
translation = str(sys.argv[2])
reference_translation = str(sys.argv[3])
file_path = str(sys.argv[4]) + '_nist_scores.csv'

nist_score = nist_score(str(reference_translation), str(translation))
print(nist_score)
if nist_score:
    print(f'text: {to_translate}\nscore: {nist_score}\n------')
    with open(file_path, 'a') as file:
        print(str(nist_score).replace('.', ','), file=file)
else:
    print('error')
    with open(file_path, 'a') as file:
        print('error in score', file=file)