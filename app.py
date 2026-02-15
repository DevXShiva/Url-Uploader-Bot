import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Bot is Running Securely!'

def run_flask():
    # Render automatically PORT environment variable deta hai
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
