import sys
import evaluate

# Get input_text from command line arguments
to_translate = str(sys.argv[1])
translation = str(sys.argv[2])
reference_translation = str(sys.argv[3])
file_path = str(sys.argv[4]) + '_meteor_scores.csv'

meteor = evaluate.load('meteor')
# translation = ["It is a guide to action which ensures that the military always obeys the commands of the party"]
# reference_translation = ["It is a guide to action that ensures that the military will forever heed Party commands"]
# Compute METEOR score
meteor_score = meteor.compute(predictions=[translation], references=[reference_translation])
meteor_score_value = meteor_score.get('meteor')

if meteor_score:
    # Print meteor_score
    print(f'text: {translation}\nmeteor: {meteor_score_value}\n------')
    with open(file_path, 'a') as file:
        print(str(meteor_score_value).replace('.', ','), file=file)
else:
    print('error')
    with open(file_path, 'a') as file:
        print('error in meteor_score', file=file)