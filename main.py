import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import requests

headless = False
# AWS LOGINS
with open("settings.json", "r") as jsonO:
    data = json.loads(jsonO.read())
    aws_login = data["aws_email"]
    aws_pass = data["aws_password"]

# Chrome stuff to avoid detection
chromeProfile = webdriver.ChromeOptions()
chromeProfile.add_argument("--disable-automation")
chromeProfile.add_argument("--no-sandbox")
chromeProfile.add_argument('--disable-extensions')
chromeProfile.add_argument('--profile-directory=Default')
chromeProfile.add_argument("--incognito")
chromeProfile.add_argument("--disable-plugins-discovery")
chromeProfile.add_argument("--start-maximized")
chromeProfile.add_experimental_option('useAutomationExtension', False)
chromeProfile.add_experimental_option(
    "excludeSwitches", ["enable-automation"])

if headless == True:
    chromeProfile.add_argument('headless')
driver = webdriver.Chrome(chrome_options=chromeProfile)

# Get website
driver.get("https://console.aws.amazon.com/transcribe/home?region=us-east-1#realTimeTranscription")

# Login
driver.find_element_by_xpath("//input[@placeholder='username@example.com']").send_keys(aws_login)
driver.find_element_by_xpath("//button[@id='next_button']").click()
time.sleep(1)

try:

    driver.find_element_by_xpath("//input[@id='password']").send_keys(aws_pass)
    driver.find_element_by_xpath("//button[@id='signin_button']").click()
    time.sleep(5)

    # Click the start streaming button
    driver.find_element_by_id("//button[@class='awsui-button awsui-button-variant-primary awsui-hover-child-icons']").click()
    # Give time for the user to actually click the allow button to access the microphone
    time.sleep(10)
except:
    print("Error while logging in please log in and start the streaming button.")
    print("Hit enter to continue")
    input()

# Access the content of the recognition
previousText = ""
while True:
    recentSection = driver.find_element_by_xpath("//div[@id='streamingContent']/div")[len(driver.find_element_by_xpath("//div[@id='streamingContent']/div"))-1].text.strip()
    #if previousText == "":
    #    newText = recentSection
    #else:
    #    newText = entireScript.replace(previousText, "")

    # previousText = entireScript
    newText = recentSection
    print(newText)
    prediction = requests.post("http://127.0.0.1:5000/gentext", json={"text": newText}).text
    print("PREDICTION: " + prediction)

    time.sleep(1)
