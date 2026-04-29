import urllib.request
import urllib.error
from flask import Flask, send_from_directory, request, Response

app = Flask(__name__, static_folder='src')


# ── ES proxy ──────────────────────────────────────────────────────────────────

@app.route('/api/es-proxy', methods=['POST'])
def es_proxy():
    es_url    = request.headers.get('X-ES-Url', '').strip().rstrip('/')
    api_key   = request.headers.get('X-ES-ApiKey', '').strip()
    es_path   = request.headers.get('X-ES-Path', '').strip().lstrip('/')
    if not es_url or not api_key or not es_path:
        return Response('Missing X-ES-Url, X-ES-ApiKey or X-ES-Path header', status=400)
    target = f'{es_url}/{es_path}'
    body   = request.get_data()
    req = urllib.request.Request(target, data=body, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', f'ApiKey {api_key}')
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            return Response(data, status=resp.status, content_type='application/json')
    except urllib.error.HTTPError as e:
        return Response(e.read(), status=e.code, content_type='application/json')
    except Exception as e:
        return Response(str(e), status=502)


# ── Static pages ──────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('src', 'comparador.html')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('src', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
