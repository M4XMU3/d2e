import sys
from transformers import BertTokenizer, BertModel
import torch
from scipy.spatial.distance import cosine
from sklearn.metrics import precision_score, recall_score, f1_score

def calculate_bert_score(candidate_text, reference_text, threshold=0.9):
    # Load pre-trained BERT model and tokenizer
    # tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    # model = BertModel.from_pretrained('bert-base-uncased')
    tokenizer = BertTokenizer.from_pretrained('bert-base-german-dbmdz-cased')
    model = BertModel.from_pretrained('bert-base-german-dbmdz-cased')

    # Tokenize the text sequences
    candidate_tokens = tokenizer(candidate_text, return_tensors='pt', padding=True, truncation=True)
    reference_tokens = tokenizer(reference_text, return_tensors='pt', padding=True, truncation=True)

    # Forward pass through the BERT model to obtain contextual embeddings
    with torch.no_grad():
        candidate_outputs = model(**candidate_tokens)
        reference_outputs = model(**reference_tokens)

    # Extract contextual embeddings from the last layer of BERT
    candidate_embeddings = candidate_outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    reference_embeddings = reference_outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

    # Ensure the embeddings are flattened to 1-D arrays
    candidate_embeddings = candidate_embeddings.reshape(candidate_embeddings.shape[0], -1)
    reference_embeddings = reference_embeddings.reshape(reference_embeddings.shape[0], -1)

    # Compute cosine similarity between candidate and reference embeddings
    similarity_scores = [1 - cosine(candidate_embeddings[i], reference_embeddings[i]) for i in range(len(candidate_embeddings))]

    # Threshold the similarity scores
    thresholded_scores = [1 if score >= threshold else 0 for score in similarity_scores]

    # Compute precision, recall, and F1 score
    precision = precision_score([1] * len(similarity_scores), thresholded_scores)
    recall = recall_score([1] * len(similarity_scores), thresholded_scores)
    f1 = f1_score([1] * len(similarity_scores), thresholded_scores)

    return precision, recall, f1

# # Example usage
# candidate_text = "Der Kater fläzte sich auf der Liegewiese."
# reference_text = "Der Kater lag auf der Wiese."

# precision, recall, f1 = calculate_bert_score(candidate_text, reference_text)
# print("Precision:", precision)
# print("Recall:", recall)
# print("F1 Score:", f1)

# get input_text from command line arguments
to_translate = str(sys.argv[1])
translation = str(sys.argv[2])
reference_translation = str(sys.argv[3])
file_path = str(sys.argv[4]) + '_bert_scores.csv'

precision, recall, f1 = calculate_bert_score(translation, reference_translation)
if f1:
    print(f'text: {to_translate}\nprecision: {precision}\nrecall: {recall}\nf1: {f1}\n------')
    with open(file_path, 'a') as file:
        print(str(precision).replace('.', ',')+";"+str(recall).replace('.', ',')+";"+str(f1).replace('.', ','), file=file)
else:
    print('error')
    with open(file_path, 'a') as file:
        print('error in score', file=file)