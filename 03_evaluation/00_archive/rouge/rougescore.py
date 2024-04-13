import sys
import evaluate

# Initialize Rouge
rouge = evaluate.load('rouge')

# Get input_text from command line arguments
# to_translate = str(sys.argv[1])
# translation = str(sys.argv[2])
# reference_translation = str(sys.argv[3])
# file_path = str(sys.argv[4]) + '_rouge_scores.csv'
translation = "Personal-Ausweis beantragen"
reference_translation = "Personal-Ausweis bestellen"

# Compute ROUGE scores
scores = rouge.compute(predictions=[translation], references=[reference_translation], rouge_types=['rouge_nl'])

if scores:
    # Print ROUGE scores to console
    print("ROUGE Scores:")
    for metric, results in scores[0].items():
        print(f"{metric}: {results['f']}")
    print("------")
    # Open the CSV file in append mode
    # with open(file_path, 'a') as file:
        # Concatenate and print ROUGE scores in one line
        # line = ';'.join(str(results['f']) for metric, results in scores[0].items())
        # print(line, file=file)
else:
    print('error')
    # Write an error message to the CSV file
    # with open(file_path, 'a') as file:
    #     print('error in score', file=file)
