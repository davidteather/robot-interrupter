###############
# API STRUCTURE
###############
# Author: David Teather
###############
# Methods
###############

# POST
###############
# URL - /gentext
# JSON = {"text": "Example Primer Text"}
# Example in testApp.py
###############
from flask import Flask, request
app = Flask(__name__)

# config
headless = False

# For the meme
@app.route('/')
def index():
  return 'You just really tried that bro. What are you even doing?'
  

# Get sentence completion from https://talktotransformer.com/ using selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

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

@app.route('/gentext', methods=['POST'])
def generate_text():
  # Clear any current text
  driver.find_element_by_xpath("//textarea[@name='prompt']").send_keys(Keys.CONTROL + "a")
  driver.find_element_by_xpath("//textarea[@name='prompt']").send_keys(Keys.DELETE)
  driver.find_element_by_xpath("//textarea[@name='prompt']").send_keys(request.json["text"])
  # Generate new text
  driver.find_element_by_xpath("//button[@class='v-btn theme--light info submit']").click()
  time.sleep(2)
  driver.find_element_by_xpath("//span[@class='v-btn__loading']").click()

  # Find response
  res = driver.find_elements_by_xpath("//div[@id='completion']/div")[1].text.strip()

  # Return Response
  return res.lower().replace(request.json["text"].lower(), "")