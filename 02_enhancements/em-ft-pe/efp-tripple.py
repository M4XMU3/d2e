# this script is based on the following tutorial:
# @misc{ai_how_nodate,
# 	title = {"{How} to give {GPT} my business knowledge?" - {Knowledge} embedding 101},
# 	url = {https://www.youtube.com/watch?v=c_nCjlSB1Zk},
# 	urldate = {2024-01-22},
# 	author = {AI, Jason},
# 	file = {"How to give GPT my business knowledge?" - Knowledge embedding 101},
# }

import sys
import os
import json
import pandas as pd
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

######
###  global vars
load_dotenv()
# message = str(sys.argv[1])
file_path = f'efp-tripple_translations.csv'
### df = Panda DataFrame
# defined as global variable so we can use it in function vectorise and later on in program itself
df = pd.read_csv('normal_easy_pairs.csv', sep=';')
### read & add rules from nls_rules.jsonl
with open('nls_rules.jsonl', 'r', encoding='utf-8') as rules_file:
    nls_rules = [line.strip() for line in rules_file]
formatted_rules = " \\\n".join(nls_rules)

######
# classes
# create a list of objects with a 'page_content' and 'metadata' attribute
class Document:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata if metadata is not None else {}

######
# functions
# vectorise the base data
def vectorise():
    # vectorize the homepages in the "pages" folder
    pages_folder = "pages"
    normal_pages = [os.path.join(pages_folder, file) for file in os.listdir(pages_folder) if file.endswith(".txt")]
    easy_pages = [os.path.join(pages_folder, file) for file in os.listdir(pages_folder) if file.endswith("-ls.txt")]
    # instantiate Document objects with metadata
    documents_normal = [Document(open(file).read()) for file in normal_pages]
    documents_easy = [Document(open(file).read()) for file in easy_pages]
    # initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings()
    # create FAISS vector stores for documents
    db_normal = FAISS.from_documents(documents_normal, embeddings)
    db_easy = FAISS.from_documents(documents_easy, embeddings)
    return db_normal, db_easy

# function for similarity search using FAISS
def retrieve_info(query):
    similar_response = db_easy.similarity_search(query, k=1)
    page_contents_array = [doc.page_content for doc in similar_response]
    return page_contents_array

# setup LLM chain
def setup_language_model_chain(message):
    # If you set `top_p` to 0.5, during text generation, for each token, the model will only consider the smallest set of tokens whose cumulative probability exceeds 0.5 (or 50%). This limits the model’s choices to the more probable tokens, leading to more coherent and focused text generation.
    # `frequency_penalty` helps to control repetition by penalizing tokens that have already been generated, thus encouraging diversity in the model output. Example configuration: Setting the `frequency_penalty` to 0.5 encourages the model to reduce the likelihood of repeating the same words or phrases within the same piece of content.
    # `presence_penalty` is similar to `frequency_penalty`, but while `frequency_penalty` reduces the likelihood of tokens appearing again based on their frequency in the text so far, `presence_penalty` discourages tokens that have already appeared, regardless of frequency. This can encourage the model to explore new topics and ideas in the continuation of the text.
    llm = ChatOpenAI(temperature=0, model="ft:gpt-3.5-turbo-1106:personal::8csRrLMi")
    template = f'Sie sind ein Übersetzer, welcher Texte, im Kontext der Landeshauptstadt München, in leichte Sprache übersetzt. \
    Dabei bleiben Sie so nahe wie möglich am Inhalt der ursprünglichen Nachricht. Sie erfinden nichts dazu was keine Relation mehr zur ursprünglichen Nachricht hat! \
    Ich nenne Ihnen zunächst alle Regeln die für die Übersetzung in leichte Sprache eingehalten werden müssen. \
    Danach werde ich Ihnen einen Text geben. Dieser muss in leichte Sprache übersetzt werden. \
    {formatted_rules} \
    Bitte in leichte Sprache übersetzen und dabei die genannten Regeln einhalten: {message}'
    # explicitly define input_variables in PromptTemplate
    prompt = PromptTemplate(input_variables=["message"], template=template)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain

# retrieval augmented generation
def generate_response(chain, message):
    best_practice = retrieve_info(message)
    # provide the 'input' argument explicitly to the invoke method
    response = chain.invoke(input={"message": message})
    return response

# refine translation to increase quality of final translation
def refine_translation(message, translation_rough):
    llm = ChatOpenAI(temperature=0, model="ft:gpt-3.5-turbo-1106:personal::8csRrLMi")
    template = f'Urspüngliche Nachricht war: {message} \
    Der folgende Text wurde von Ihnen bereits in leichte Sprache übersetzt: {translation_rough} \
    Oft entsteht dabei jedoch eine nicht zufriedenstellende Übersetzung. Sie kontrollieren daher die Übersetzung erneut und achten dabei auf folgende Punkte speziell: \
    * Sie entfernen alle mehrfachen identischen Wiederholungen eines Satzes! \
    * Sie beschränken die Übersetzung auf das wesentliche und achten auf die Länge! \
    * Sie stellen sicher, dass die Übersetzung nicht mehr als drei Beispiele bzw. Bullet Points je zu erklärendem Begriff enthält! \
    * Sie geben auf keinen Fall die Regeln zur Übersetzung direkt aus! \
    * Sie übersetzen erneut, falls der ursprüngliche Text mit der Übersetzung identisch ist! \
    * Sie erfinden keine Informationen dazu, die nicht im Aussgangstext stehen!'
    # explicitly define input_variables in PromptTemplate
    prompt = PromptTemplate(input_variables=["message"], template=template)
    chain = LLMChain(llm=llm, prompt=prompt)
    
    best_practice = retrieve_info(message)
    # provide the 'input' argument explicitly to the invoke method
    response = chain.invoke(input={"message": message})
    return response

# refine translation to increase quality of final translation
def refine_again_translation(message, translation_better):
    llm = ChatOpenAI(temperature=0, model="ft:gpt-3.5-turbo-1106:personal::8csRrLMi")
    template = f'Urspüngliche Nachricht war: {message} \
    Der folgende Text wurde von Ihnen bereits in leichte Sprache übersetzt: {translation_better} \
    Oft entsteht dabei jedoch eine nicht zufriedenstellende Übersetzung. Sie kontrollieren daher die Übersetzung erneut und achten dabei auf folgende Punkte speziell: \
    * Sie entfernen alle mehrfachen identischen Wiederholungen eines Satzes! \
    * Sie entfernen alle Beispiele ab dem vierten Beispiel!'   
    # explicitly define input_variables in PromptTemplate
    prompt = PromptTemplate(input_variables=["message"], template=template)
    chain = LLMChain(llm=llm, prompt=prompt)
    
    best_practice = retrieve_info(message)
    # provide the 'input' argument explicitly to the invoke method
    response = chain.invoke(input={"message": message})
    return response

######
# program
# vectorise data
db_normal, db_easy = vectorise()

# Iterate over each row in the DataFrame (= the base csv)
for index, row in df.iterrows():
    message = row['normal']

# create chain
chain = setup_language_model_chain(message)
# Access the 'normal' column value in each row
# Call the translate function with the 'normal' text
translation_rough = generate_response(chain, message)['text']
# to improve quality refine translation by LLM itself
translation_better = refine_translation(message, translation_rough)
# to improve quality refine translation by LLM itself AGAIN
translation = refine_again_translation(message, translation_better)
# print to console as debug/log function
print(f'{translation}\n------')

    # # add translation to output file
    # if translation:
    #     # replace newline with literal \n string so that in CSV translation stays in one field
    #     translation = translation['text'].replace('\n', '\\n')
    #     with open(file_path, 'a') as file:
    #         print(f"{message};{translation}", file=file)
    # else:
    #         print('error in translation', file=file)