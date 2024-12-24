from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import requests
import os

def fetch_trending_topics():
    # ProxyMesh setup
    proxy_url = os.getenv("PROXY_URL")
    proxies = {"http": proxy_url, "https": proxy_url}

    # Selenium WebDriver setup
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver_path = "path/to/chromedriver"  # Update with your ChromeDriver path
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # Login to Twitter
    driver.get("https://twitter.com/login")
    driver.find_element(By.NAME, "username").send_keys(os.getenv("TWITTER_USERNAME"))
    driver.find_element(By.NAME, "password").send_keys(os.getenv("TWITTER_PASSWORD"))
    driver.find_element(By.XPATH, "//div[contains(text(),'Log in')]").click()

    # Fetch trending topics
    driver.get("https://twitter.com")
    trending_topics = driver.find_elements(By.XPATH, "//section//span")[:5]
    trends = [topic.text for topic in trending_topics]

    # Close the driver
    driver.quit()

    # Prepare result
    result = {
        "unique_id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "trends": trends,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip_address": requests.get("https://api.ipify.org", proxies=proxies).text
    }
    return result
