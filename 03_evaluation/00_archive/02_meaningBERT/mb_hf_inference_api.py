import requests

API_URL = "https://api-inference.huggingface.co/models/davebulaval/MeaningBERT"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": "dsfadsf adsf. I love you.",
})

print(output)
