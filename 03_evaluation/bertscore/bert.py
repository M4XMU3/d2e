import sys
from evaluate import load

# # Example usage
# candidate_text = "Der Kater fläzte sich auf der Liegewiese."
# reference_text = "Der Kater lag auf der Wiese."

# get input_text from command line arguments
to_translate = str(sys.argv[1])
translation = str(sys.argv[2])
reference_translation = str(sys.argv[3])
file_path = str(sys.argv[4]) + '_bert_scores.csv'

bertscore = load("bertscore")
bert_results = bertscore.compute(predictions=[translation], references=[[reference_translation]], lang="de")

if bert_results:
    # Print the values for precision, recall, and f1 separated by ";"
    print(f'text: {translation}\n'+';'.join([str(bert_results.get('precision')[0]), str(bert_results.get('recall')[0]), str(bert_results.get('f1')[0])])+'\n------')
    with open(file_path, 'a') as file:
        # print(str(precision).replace('.', ',')+";"+str(recall).replace('.', ',')+";"+str(f1).replace('.', ','), file=file)
        print(';'.join([str(bert_results.get('precision')[0]).replace('.', ','), str(bert_results.get('recall')[0]).replace('.', ','), str(bert_results.get('f1')[0]).replace('.', ',')]), file=file)
else:
    print('error')
    with open(file_path, 'a') as file:
        print('error in score', file=file)