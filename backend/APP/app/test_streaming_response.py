import requests

url = "http://127.0.0.1:5000/advisor/stream"
data = {
    "profile_description": "Experienced frontend developer",
    "target_job_title": "Senior Backend Engineer"
}

with requests.post(url, json=data, stream=True) as response:
    buffer = ""
    for chunk in response.iter_content(chunk_size=1, decode_unicode=True):
        if chunk:
            buffer += chunk
            if chunk.isspace():
                print(buffer, end="", flush=True)
                buffer = ""
    # print any remaining buffer
    if buffer:
        print(buffer, end="", flush=True)

