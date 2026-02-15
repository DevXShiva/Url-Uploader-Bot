import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    # Ye page Render check karega health status ke liye
    return 'Bot is Running Securely!'

# Iska naam 'run_server' hona chahiye taaki bot.py ise dhoond sake
def run_server():
    # Render default port 10000 use karta hai
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    run_server()
