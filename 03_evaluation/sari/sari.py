import sys
from evaluate import load

sari = load("sari")
sources=[ "" + sys.argv[1] ]
predictions=[ "" + sys.argv[2] ]
references=[[ "" + sys.argv[3] ]]
file_path=str(sys.argv[4]) + '_sari_scores.csv'
sari_score = sari.compute(sources=sources, predictions=predictions, references=references)

# print(sources)
print(predictions)
# print(references)
print(str(sari_score['sari']/100).replace('.', ','))
print('------')

if sari_score:
   with open(file_path, 'a') as file:
       print(str(sari_score['sari']/100).replace('.', ','), file=file)
else:
       print('error in calculating sari score', file=file)
