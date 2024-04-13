import sys
from evaluate import load
ter = load("ter")
to_translate=[ "" + sys.argv[1] ]
predictions=[ "" + sys.argv[2] ]
references=[[ "" + sys.argv[3] ]]

file_path=str(sys.argv[4]) + '_ter_scores.csv'
ter_score = ter.compute(predictions=predictions, references=references, case_sensitive=True)


print(predictions)
# print(references)
print(ter_score['score'])
print('------')

if ter_score:
    with open(file_path, 'a') as file:
        # print(ter_score, file=file)
        # Concatenate and print scores in one line
        print(';'.join([str(ter_score['score']).replace('.', ','), str(ter_score['num_edits']).replace('.', ','), str(ter_score['ref_length']).replace('.', ',')]), file=file)
else:
        print('error in calculating ter score', file=file)
