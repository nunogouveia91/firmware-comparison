from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='src')


@app.route('/')
def index():
    return send_from_directory('src', 'comparador.html')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('src', filename)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
