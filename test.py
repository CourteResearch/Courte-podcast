import requests

url = "https://api.braintrust.dev/v1/proxy/chat/completions"
headers = {
    "Authorization": "Bearer sk-os6REk1CtTQK3HPi0vygHE9GB90QQAoBASpyFO773WGGROTC",  # Replace with your actual key
    "Content-Type": "application/json"
}
data = {
    "model": "claude-3-5-sonnet-20240601",
    "messages": [
        {"role": "system", "content": "You are a senior software engineer who writes clean and efficient code."},
        {"role": "user", "content": "Write a Python function that calculates factorial recursively."}
    ],
    "max_tokens": 300,
    "temperature": 0.2
}

response = requests.post(url, headers=headers, json=data)

print("Status code:", response.status_code)
print(response.json()["choices"][0]["message"]["content"])
