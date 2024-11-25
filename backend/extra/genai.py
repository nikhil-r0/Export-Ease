
import requests

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-1B"
headers = {"Authorization": "Bearer token"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": "Can you please let us know more details about your ",
})

print(output)