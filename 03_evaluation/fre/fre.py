import sys
#import textstat
from textstat import textstat

translation=('' + sys.argv[2])
file_path=('' + str(sys.argv[4]) + '_fre_scores.csv')

# set to German
textstat.set_lang('de')

# calculate metrics
flesch_re_score = str(textstat.flesch_reading_ease(translation)).replace('.', ',')
fkgl_score = str(textstat.flesch_kincaid_grade(translation)).replace('.', ',')

print(translation)
print('flesch_re: ' + str(flesch_re_score))
print('fkgl: ' + str(fkgl_score))
print('------')

if flesch_re_score:
    with open(file_path, 'a') as file:
        print(f"{flesch_re_score}; {fkgl_score}", file=file)
else:
        print('error in calculating score', file=file)

