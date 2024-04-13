import sys

def compute_meteor(hypothesis, reference):
    # Tokenize hypothesis and reference
    hypothesis_tokens = hypothesis.split()
    reference_tokens = reference.split()

    # Compute matches
    matches = 0
    for token in hypothesis_tokens:
        if token in reference_tokens:
            matches += 1

    # Compute precision and recall
    precision = matches / len(hypothesis_tokens)
    recall = matches / len(reference_tokens)

    # Compute METEOR score (using harmonic mean of precision and recall)
    if precision + recall == 0:
        meteor_score = 0  # Avoid division by zero
    else:
        meteor_score = (precision * recall) / (precision + recall)

    return meteor_score

# Sample system and reference translations
# system_translation = "ROUGE is a package for evaluating summarization tasks."
# reference_translation = "ROUGE is a tool for evaluating automatic summarization tasks."
# Get input_text from command line arguments
to_translate = str(sys.argv[1])
translation = str(sys.argv[2])
reference_translation = str(sys.argv[3])
file_path = str(sys.argv[4]) + '_meteor_scores.csv'

# Compute METEOR score
meteor_score = compute_meteor(translation, reference_translation)

if meteor_score:
    # Print meteor_score
    print(f'text: {to_translate}\nmeteor: {meteor_score}\n------')
    with open(file_path, 'a') as file:
        print(str(meteor_score).replace('.', ','), file=file)
else:
    print('error')
    with open(file_path, 'a') as file:
        print('error in meteor_score', file=file)