from flask import Flask

app = Flask(__name__)


@app.route('/')
def main():
    return "<h2>This is my app!</h2>"