import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json

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
driver.get("https://talktotransformer.com/")


# Example deepspeech command
# os.system("deepspeech --model deepspeech-0.6.1-models/output_graph.pbmm --audio test.wav")