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
file_path = f'ft-pe-twice_translations.csv'
### df = Panda DataFrame
# defined as global variable so we can use it in function vectorise and later on in program itself
df = pd.read_csv('normal_easy_pairs.csv', sep=';')
### read & add rules from nls_rules.jsonl
with open('nls-rules.txt', 'r', encoding='utf-8') as rules_file:
    nls_rules = [line.strip() for line in rules_file]
formatted_rules = " \\\n".join(nls_rules)


# setup LLM chain
def setup_language_model_chain(message):
    # If you set `top_p` to 0.5, during text generation, for each token, the model will only consider the smallest set of tokens whose cumulative probability exceeds 0.5 (or 50%). This limits the model’s choices to the more probable tokens, leading to more coherent and focused text generation.
    # `frequency_penalty` helps to control repetition by penalizing tokens that have already been generated, thus encouraging diversity in the model output. Example configuration: Setting the `frequency_penalty` to 0.5 encourages the model to reduce the likelihood of repeating the same words or phrases within the same piece of content.
    # `presence_penalty` is similar to `frequency_penalty`, but while `frequency_penalty` reduces the likelihood of tokens appearing again based on their frequency in the text so far, `presence_penalty` discourages tokens that have already appeared, regardless of frequency. This can encourage the model to explore new topics and ideas in the continuation of the text.
    llm = ChatOpenAI(temperature=0, model="ft:gpt-3.5-turbo-1106:personal::8csRrLMi")
    template = f'Sie sind ein Übersetzer, welcher Texte, im Kontext der Landeshauptstadt München, in Leichte Sprache übersetzt. \
    Die Übersetzungen werden genutzt um den Basistext Menschen mit Behinderung zugänglich zu machen. \
    Komposita wie "Personalausweis" müssen in z.B. "Personal-Ausweis" aufgeteilt werden. \
    Falls Beispiele nötig sind um einen Sachverhalt zu erklären, geben Sie maximal drei Beispiele an. \
    Bei der Übersetzung bleiben Sie so nahe wie möglich am Inhalt der ursprünglichen Nachricht. Sie erfinden nichts dazu was keine Relation mehr zur ursprünglichen Nachricht hat! \
    Ich nenne Ihnen zunächst alle Regeln die für die Übersetzung in Leichte Sprache eingehalten werden müssen. \
    Danach werde ich Ihnen einen Text geben. Dieser muss in Leichte Sprache übersetzt werden. Nun die Regeln: \
    {formatted_rules} \
    Folgendes bitte in Leichte Sprache übersetzen und dabei die genannten Regeln einhalten: {message}'
    # explicitly define input_variables in PromptTemplate
    prompt = PromptTemplate(input_variables=["message"], template=template)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain

# retrieval augmented generation
def generate_response(chain, message):
    # provide the 'input' argument explicitly to the invoke method
    response = chain.invoke(input={"message": message})
    return response

# refine translation to increase quality of final translation
def refine_translation(message, translation_rough):
    llm = ChatOpenAI(temperature=0, model="ft:gpt-3.5-turbo-1106:personal::8csRrLMi")
    template = f'Sie sind ein Übersetzer, welcher Texte, im Kontext der Landeshauptstadt München, in Leichte Sprache übersetzt. \
    Die Übersetzungen werden genutzt um den Basistext Menschen mit Behinderung zugänglich zu machen. \
    Der folgende Text wurde von Ihnen bereits in Leichte Sprache übersetzt: {translation_rough} \
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
    
    # provide the 'input' argument explicitly to the invoke method
    response = chain.invoke(input={"message": message})
    return response

######
# program
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
        # translation = translation.replace('\n', '\\n')
        translation = translation['text'].replace('\n', '\\n')
        with open(file_path, 'a') as file:
            print(f"{message};{translation}", file=file)
    else:
            print('error in translation', file=file)