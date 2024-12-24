from flask import Flask, render_template, jsonify
from selenium_script import run_selenium_script
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb+srv://vinodkr8833:12345@cluster0.clwno.mongodb.net/")
db = client['selenium_db']
collection = db['script_results']

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run-script", methods=["GET"])
def run_script():
    # Run Selenium script and fetch result
    result = run_selenium_script()
    
    # Fetch the latest MongoDB document for display
    latest_record = collection.find_one(sort=[("_id", -1)])
    latest_record["_id"] = str(latest_record["_id"])  # Convert ObjectId to string for JSON serialization

    return render_template(
        "results.html",
        trends=result,
        json_extract=latest_record
    )

if __name__ == "__main__":
    app.run(debug=True)