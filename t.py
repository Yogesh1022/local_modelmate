# import secrets
# print(secrets.token_urlsafe(32))  # Generates a secure random string
import requests

token = "dDC6_44ms5iNrU69A-nIwddxTmrw1suM7BiuYQTB4m0"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

payload = {
    "prompt": "Explain Agile methodology in software development.",
    "prompt_type": "sdlc"
}

url = "http://127.0.0.1:8000/api/prompt/process"
response = requests.post(url, headers=headers, json=payload)

print(response.status_code)
print(response.json())
