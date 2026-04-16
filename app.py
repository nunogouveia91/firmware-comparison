from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='src')


# ── Static pages ──────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('src', 'comparador.html')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('src', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
