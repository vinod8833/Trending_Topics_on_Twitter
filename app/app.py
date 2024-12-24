from flask import Flask, render_template, jsonify
from selenium_script import fetch_trending_topics
from db_config import insert_to_db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script', methods=['GET'])
def run_script():
    result = fetch_trending_topics()
    insert_to_db(result)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
