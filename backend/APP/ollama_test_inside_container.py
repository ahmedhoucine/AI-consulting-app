import httpx

url = "http://host.docker.internal:11434"

try:
    response = httpx.get(url, timeout=5.0)
    print("Status code:", response.status_code)
    print("Response text:", response.text)
except Exception as e:
    print("Error:", e)
