import sys
#import textstat
from textstat import textstat

test_data=('' + sys.argv[1])
file_path=('' + str(sys.argv[2]) + '_wstf_scores.csv')

# set to German
textstat.set_lang('de')

# calculate metrics
wstf_score = str(textstat.wiener_sachtextformel(test_data, 4)).replace('.', ',')

print(test_data)
print('WSTF: ' + wstf_score)

if wstf_score:
    with open(file_path, 'a') as file:
        print(f"{wstf_score}", file=file)
else:
        print('error in calculating score', file=file)

