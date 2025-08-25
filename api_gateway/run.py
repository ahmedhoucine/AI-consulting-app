from flask import Flask, request, jsonify
import requests
import consul

app = Flask(__name__)
c = consul.Consul()

def get_service_url(service_name):
    services = c.catalog.service(service_name)[1]
    if not services:
        raise Exception(f"Service {service_name} not found")
    svc = services[0]
    return f"http://{svc['ServiceAddress']}:{svc['ServicePort']}"

@app.route("/api/<service>/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def proxy(service, path):
    try:
        base_url = get_service_url(f"{service}-service")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    url = f"{base_url}/{path}"
    resp = requests.request(
        method=request.method,
        url=url,
        headers={k: v for k, v in request.headers if k != "Host"},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    return (resp.content, resp.status_code, resp.headers.items())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
