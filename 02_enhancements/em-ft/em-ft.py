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
file_path = f'em-ft-twice_translations.csv'
### df = Panda DataFrame
# defined as global variable so we can use it in function vectorise and later on in program itself
df = pd.read_csv('normal_easy_pairs.csv', sep=';')

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
    # low k-value to decreased computational demands
    similar_response = db_easy.similarity_search(query, k=1)
    page_contents_array = [doc.page_content for doc in similar_response]
    return page_contents_array

# setup LLM chain
def setup_language_model_chain(message):
    # If you set `top_p` to 0.5, during text generation, for each token, the model will only consider the smallest set of tokens whose cumulative probability exceeds 0.5 (or 50%). This limits the model’s choices to the more probable tokens, leading to more coherent and focused text generation.
    # `frequency_penalty` helps to control repetition by penalizing tokens that have already been generated, thus encouraging diversity in the model output. Example configuration: Setting the `frequency_penalty` to 0.5 encourages the model to reduce the likelihood of repeating the same words or phrases within the same piece of content.
    # `presence_penalty` is similar to `frequency_penalty`, but while `frequency_penalty` reduces the likelihood of tokens appearing again based on their frequency in the text so far, `presence_penalty` discourages tokens that have already appeared, regardless of frequency. This can encourage the model to explore new topics and ideas in the continuation of the text.
    llm = ChatOpenAI(temperature=0, model="ft:gpt-3.5-turbo-1106:personal::8csRrLMi")
    template = "Diese Beispielübersetzung kommt einer Übersetzung des Eingabetextes in leichte Sprache am nähesten: '{example_translation}'. Bitte übersetzen Sie den folgenden Eingabetext entsprechend in leichte Sprache: '{message}'"
    # Explicitly define input_variables in PromptTemplate
    prompt = PromptTemplate(input_variables=["message", "example_translation"], template=template)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain

# retrieval augmented generation
def generate_response(chain, message):
    retrieve_info_output = retrieve_info(message)
    # Provide the 'input' argument explicitly to the invoke method
    # Here, {retrieve_info_output} is the retrieved information that guides the model in generating the response
    response = chain.invoke(input={'message': message, 'example_translation': retrieve_info_output[0]})
    return response

# refine translation to increase quality of final translation
def refine_translation(message, translation_rough):
    llm = ChatOpenAI(temperature=0, model="ft:gpt-3.5-turbo-1106:personal::8csRrLMi")
    template = f'Sie sind ein Übersetzer, welcher Texte, im Kontext der Landeshauptstadt München, in leichte Sprache übersetzt. \
    Die Übersetzungen werden genutzt um den Basistext Menschen mit Behinderung zugänglich zu machen. \
    Der folgende Text wurde von Ihnen bereits in leichte Sprache übersetzt: {translation_rough} \
    Der urspüngliche Text vor der Übersetzung war: {message} \
    Sie müssen Ihre erste Übersetzung erneut kontrollieren und dabei auf folgende Punkte speziell achten: \
    * Sie entfernen alle mehrfachen identischen Wiederholungen eines Satzes! \
    * Sie beschränken die Übersetzung auf das wesentliche und kürzen diese, falls sinnlos Text-Patterns oder Beispiele wiederholt werden, die keine wesentlich neuen Informationen beitragen! \
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


######
# program
# vectorise data
db_normal, db_easy = vectorise()


# message = "In der Stadt-Information im Rathaus erhalten Sie neben Printmedien, Rat und Hilfeleistung verschiedenster Art."
# message = "In der Stadt-Information im Rathaus erhalten Sie Prospekte, Informationsmaterial und Formulare zu unterschiedlichen Themen. Die Mitarbeiter stehen den Besucherinnen und Besucher mit Rat und Hilfeleistung verschiedenster Art zur Verfügung."
# message = "Bei der Behördennummer wird der persönliche Kontakt groß geschrieben. Von Montag bis Freitag, 8 bis 18 Uhr, können den Mitarbeitenden der 115-Servicecenter Fragen gestellt werden. Die meisten Anliegen werden direkt beantwortet. Falls dies einmal nicht möglich ist, verspricht die 115 eine schnelle Rückmeldung."


# Iterate over each row in the DataFrame (= the base csv)
for index, row in df.iterrows():
    message = row['normal']
    # create chain
    chain = setup_language_model_chain(message)
    # Access the 'normal' column value in each row
    # Call the translate function with the 'normal' text
    translation_rough = generate_response(chain, message)['text']
    # to improve quality refine translation by LLM itself
    translation = refine_translation(message, translation_rough)
    # print to console as debug/log function
    print(f'{translation}\n------')

    # add translation to output file
    if translation:
        # replace newline with literal \n string so that in CSV translation stays in one field
        # translation = translation.replace('\n', '\\n') # one time translation
        translation = translation['text'].replace('\n', '\\n') # translation after refinement
        with open(file_path, 'a') as file:
            print(f"{message};{translation}", file=file)
    else:
            print('error in translation', file=file)