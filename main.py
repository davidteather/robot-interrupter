import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import requests
import pygame
from gtts import gTTS 

pygame.mixer.init()
headless = False
# AWS LOGINS
with open("settings.json", "r") as jsonO:
    data = json.loads(jsonO.read())
    aws_login = data["aws_email"]
    aws_pass = data["aws_password"]

# Setup ML
import gpt_2_simple as gpt2

# Download model if not exists
model_name = "355M"
if not os.path.isdir(os.path.join("models", model_name)):
	print(f"Downloading {model_name} model...")
	gpt2.download_gpt2(model_name=model_name)

# Start model instance
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess)
print("Loaded Model")

def generateML(primer):
    return gpt2.generate(sess, length=75, prefix=primer, return_as_list=True, include_prefix=False)[0].lower().replace(primer.lower(), "")


# TODO: CHANGE TO ACTUAL GOOD AWS https://docs.aws.amazon.com/transcribe/latest/dg/API_streaming_StartStreamTranscription.html

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
var = False
while True:
    try:
        recentSection = driver.find_elements_by_xpath("//div[@id='streamingContent']/div")[len(driver.find_elements_by_xpath("//div[@id='streamingContent']/div"))-2].text.strip()
    except:
        recentSection = driver.find_elements_by_xpath("//div[@id='streamingContent']/div")[len(driver.find_elements_by_xpath("//div[@id='streamingContent']/div"))-1].text.strip()
    #if previousText == "":
    #    newText = recentSection
    #else:
    #    newText = entireScript.replace(previousText, "")

    # previousText = entireScript
    newText = recentSection
    print(newText)

    if newText != "":
        predictionText = generateML(newText).replace("<|endoftext|>", "")
        print("PREDICTION: " + predictionText)
        # generate the TTS
        myobj = gTTS(text=predictionText, lang='en', slow=False) 

        try:
            myobj.save("tmp.mp3")
            pygame.mixer.music.load("tmp.mp3")
            pygame.mixer.music.play()
            time.sleep(3)
            var = True
        except:
            myobj.save("tmp2.mp3")
            pygame.mixer.music.load("tmp2.mp3")
            pygame.mixer.music.play()
            time.sleep(3)
            var = True

    if not var:
        time.sleep(2)
    
