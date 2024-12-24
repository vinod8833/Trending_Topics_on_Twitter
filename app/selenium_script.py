import uuid
from datetime import datetime
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
import socket
from flask import Flask, jsonify

app = Flask(__name__)

def run_selenium_script():
    # MongoDB setup
    client = MongoClient("mongodb://localhost:27017/")
    db = client['selenium_db']
    collection = db['script_results']

    # Generate unique ID
    unique_id = str(uuid.uuid4())

    # Selenium setup
    driver = webdriver.Chrome()  # Ensure ChromeDriver is installed
    driver.get("http://127.0.0.1:5000/")  # Replace with the actual URL

    # Scrape trends (Example: Replace with actual selectors)
    trends = [driver.find_element(By.XPATH, f"//xpath{i}").text for i in range(1, 6)]

    # Get IP address
    ip_address = socket.gethostbyname(socket.gethostname())

    # Get current date and time
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Prepare data
    data = {
        "unique_id": unique_id,
        "nameoftrend1": trends[0],
        "nameoftrend2": trends[1],
        "nameoftrend3": trends[2],
        "nameoftrend4": trends[3],
        "nameoftrend5": trends[4],
        "date_time": end_time,
        "ip_address": ip_address
    }

    # Save to MongoDB
    collection.insert_one(data)
    driver.quit()

    return data

@app.route('/run_script', methods=['GET'])
def run_script():
    try:
        result = run_selenium_script()
        
        # Fetch the latest record from MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client['selenium_db']
        collection = db['script_results']
        latest_record = collection.find_one(sort=[("_id", -1)])  # Fetch the latest record

        # Check if record exists
        if latest_record:
            latest_record["_id"] = str(latest_record["_id"])  # Convert ObjectId to string for JSON serialization
            return jsonify(latest_record)
        else:
            return jsonify({"error": "No records found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
