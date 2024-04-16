# d2e
Difficult To Easy - Developing a LLM for translating official into Easy Language            
paper: Arxive link coming soon

This work aims to enhance GPT with Embedding, Fine Tuning, Prompt Engineering and the combination of these methods. Furthermore, it evaluates the results of the translations of the parallel corpora base data into German Easy Language.                   
To use these scripts you need an OpenAI Account.              

# before you start
* this porject is meant to be used in a Linux or at least WSL System
* if there are files in folders that appear to be 0kb they are symlinks

# How To - Translation & Evaluation
* create python venv && activate
* install requirements-python.txt with pip
* insert your OpenAI API key in the .env file
* ./02_enhancements/ contains all enhancement methods
  * each method folder contains, named after the method
    * a python script that calculates the Translation
    * a shell script that shows how to call the python script for your own tests
    * the later can be used to calculate the translations of all 170 base texts in ./02_enhancements/to_translate.txt
* ./03_evaluation/ works in the same way but for evaluating the translations
