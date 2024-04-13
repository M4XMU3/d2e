import requests
import time

API_URL = "https://api-inference.huggingface.co/models/deepset/gbert-base"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": "The answer to the universe is undefined.",
})
time.sleep(20)
print(output)