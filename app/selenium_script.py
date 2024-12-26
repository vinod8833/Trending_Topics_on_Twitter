from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import uuid
from datetime import datetime
from pymongo import MongoClient
import socket

def run_selenium_script():
    client = MongoClient("_________________")
    db = client['selenium_db']
    collection = db['script_results']

    unique_id = str(uuid.uuid4())

    options = Options()
    options.headless = True  
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("http://127.0.0.1:5000/")  
        
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        trends = ["#KisanKaKamaal Under 10k Tweets",
                  "#10_Saal_Dilli_Behaal Under 10k Tweets",
                  "#चौधरी चरण सिंह 49.5k Tweets",
                  "#BjpDelhiWantNewCandidate Under 10k Tweets",
                  "#ManmohanSingh"]
        for i in range(1, 6):
            try:
                trend_element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, f"//div[@class='trend-{i}']"))
                )
                trends.append(trend_element.text)
            except Exception as e:
                trends.append(f"Trend {i} not found: {str(e)}")

        ip_address = socket.gethostbyname(socket.gethostname())
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
        print(data)
        
        collection.insert_one(data)
    
    except Exception as e:
        return {"error": f"Script failed: {str(e)}"}
    
    finally:
        driver.quit() 

    return {"result": "Script completed successfully", "data": data}