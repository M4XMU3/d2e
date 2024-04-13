import sys
from nltk.tokenize import word_tokenize
from collections import Counter
import nltk
nltk.download('punkt')  # Download the NLTK punkt data

# prediction=str(sys.argv[2])
prediction = "Wie lange gilt der Park-Ausweis?\nDer Park-Ausweis gilt höchstens 5 Jahre.\nDanach müssen Sie einen neuen Park-Ausweis beantragen.\n\nWas müssen Sie tun, wenn Sie einen neuen Park-Ausweis brauchen?\nSie müssen einen neuen Park-Ausweis beantragen.\nDas bedeutet:\nSie müssen einen Brief schreiben.\nDen Brief schicken Sie an das Kreis-Verwaltungs-Referat.\nDie Abkürzung dafür ist KVR.\nIn dem Brief müssen Sie schreiben:\n* Ihren Vor-Namen und Ihren Nach-Namen.\n* Ihre Adresse.\n* Ihr Geburts-Datum.\n* Dass Sie einen neuen Park-Ausweis für Menschen mit Behinderung bekommen möchten.\n* Dass Sie Ihren Haupt-Wohnsitz in München haben.\n* Dass Sie eine schwere Behinderung haben.\n* Dass Sie einen Schwer-Behinderten-Ausweis haben.\n  Wenn Sie einen Schwer-Behinderten-Ausweis haben.\n  Dann müssen Sie das in dem Brief schreiben.\n  Sie müssen auch eine Kopie von Ihrem Schwer-Behinderten-Ausweis in den Brief legen.\n  Eine Kopie ist eine Fotokopie.\n  Eine Fotokopie ist ein Blatt Papier.\n  Auf dem Blatt Papier ist das gleiche Bild wie auf dem Schwer-Behinderten-Ausweis.\n  Sie müssen auf die Fotokopie schreiben:\n  Das ist eine Kopie.\n  Und Sie müssen auf die Fotokopie schreiben:\n  Ich beantrage einen neuen Park-Ausweis für Menschen mit Behinderung.\n  Und Sie müssen auf die Fotokopie schreiben:\n  Ich habe meinen Haupt-Wohnsitz in München.\n  Und Sie müssen auf die Fotokopie schreiben:\n  Ich habe eine schwere Behinderung.\n  Und Sie müssen auf die Fotokopie schreiben:\n  Ich habe einen Schwer-Behinderten-Ausweis."
# file_path=str(sys.argv[4]) + '_ttr_scores.csv'

def calculate_ttr(text):
    # Tokenize the text
    # tokens = word_tokenize(text.lower())
    tokens = word_tokenize(text.lower(), language='german')

    # Calculate the number of types (unique words)
    num_types = len(set(tokens))

    # Calculate the total number of tokens (words)
    num_tokens = len(tokens)

    # Calculate TTR
    ttr = num_types / num_tokens

    # Calculate TTR
    if num_tokens > 0:
       ttr = num_types / num_tokens

       return num_tokens, num_types, ttr
    return num_tokens, num_types, 0
# Calculate and print TTR
num_tokens, num_types, ttr_score = calculate_ttr(prediction)
print(prediction)
print(f"TTR: {ttr_score}")
print('------')

# if ttr_score:
#     with open(file_path, 'a') as file:
#         print(f'{num_tokens};{num_types};{ttr_score}', file=file)
# else:
#         print('error in calculating score', file=file)
