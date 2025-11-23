import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Flask will look for 'index.html' in the 'templates' folder.
    return render_template('index.html')

if __name__ == '__main__':
    # Render provides the PORT environment variable
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
