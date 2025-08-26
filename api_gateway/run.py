from flask import Flask, request, jsonify, Response, stream_with_context
import requests
import consul
from flask_cors import CORS

# Constants
ALLOWED_ORIGIN = "http://localhost:4200"

app = Flask(__name__)
c = consul.Consul()

# Enable CORS globally
CORS(app, resources={r"/*": {"origins": ALLOWED_ORIGIN}}, supports_credentials=True)


def get_service_url(service_name: str) -> str:
    """Get the service address and port from Consul"""
    services = c.catalog.service(service_name)[1]
    if not services:
        raise Exception(f"Service {service_name} not found")
    svc = services[0]
    return f"http://{svc['ServiceAddress']}:{svc['ServicePort']}"


@app.route("/api/<service>/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def proxy(service, path):
    # Handle CORS preflight
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        response.headers.update({
            "Access-Control-Allow-Origin": ALLOWED_ORIGIN,
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
        })
        return response

    # Lookup service in Consul
    try:
        base_url = get_service_url(f"{service}-service")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    url = f"{base_url}/{path}"

    req = requests.request(
        method=request.method,
        url=url,
        headers={k: v for k, v in request.headers if k.lower() != "host"},
        data=request.get_data(),
        cookies=request.cookies,
        stream=True,
    )

    def generate():
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                yield chunk

    headers = dict(req.headers)
    headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN

    return Response(stream_with_context(generate()), status=req.status_code, headers=headers)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
