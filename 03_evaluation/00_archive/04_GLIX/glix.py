import sys
#import textstat
from textstat import textstat

test_data=('' + sys.argv[1])
file_path=('' + str(sys.argv[2]) + '_glix_scores.csv')

# set to German
textstat.set_lang('de')

# calculate metrics
gunning_fog_score = str(textstat.gunning_fog(test_data)).replace('.', ',')

print(test_data)
print('gunning fog: ' + str(gunning_fog_score))

if gunning_fog_score:
    with open(file_path, 'a') as file:
        print(f"{gunning_fog_score}", file=file)
else:
        print('error in calculating score', file=file)

