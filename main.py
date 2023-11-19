from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import time
#import parse_image_percentage
import openai_vision

# Setup Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
# OpenAI API Key
api_key = "API_KEY_HERE"

# Navigate to Google
driver.get("http://www.google.com")

# Find the search box and enter the query
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Goodlife fitness liberty village")
search_box.send_keys(Keys.RETURN)

# Wait for the page to load
time.sleep(5)

# Locate your element
# Use a relative locator method
# Initial Element: Popular times
initial_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Popular times')]")

# Navigate two levels up and then to the following sibling to find the Graph element
parent_of_container = initial_element.find_element(By.XPATH, "./ancestor::div[2]")
container_element = initial_element.find_element(By.XPATH, "./ancestor::div[2]/following-sibling::div")
# Assuming target_element is the element you previously located
first_child_div = container_element.find_element(By.XPATH, "./div")

# Now graph_element refers to the second div sibling of the first child of target_element
target_element = first_child_div.find_element(By.XPATH, "following-sibling::div[1]")
# Scroll to the element
driver.execute_script("arguments[0].scrollIntoView();", parent_of_container)

# Wait for a moment after scrolling
time.sleep(2)

# Get the element's location using JavaScript
rect = driver.execute_script("return arguments[0].getBoundingClientRect();", container_element)

# Take a screenshot of the entire page
driver.save_screenshot("pageImage.png")

# Calculate the element's position and size
x = rect['x']
y = rect['y']
width = rect['width']
height = rect['height']

# Crop the screenshot to the element
im = Image.open("pageImage.png")
im = im.crop((int(x), int(y), int(x + width), int(y + height)))
im.save("elementScreenshot.png")

# Close the browser
driver.quit()

# Call OpenAI API with image, get "Live: [text]" response
api_key = "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"
image_path = "elementScreenshot.png"
response_content = openai_vision.process_image_and_get_response(image_path, api_key)
print(response_content)

# orange: #f28b82
# grey: #5f6368

#AGENT CONFIG
# The Graph Interpreter is designed to analyze images of Google Popular Times graphs. Its primary function is to parse these images, focusing specifically on:

# 1. The 'Live: ' text
# 2. .Give a rough estimate of the size of the orange 'Live' bar in relation to the bar behind it in the graph. Please provide an approximate percentage based on visual assessment, understanding that it's a subjective estimate and not an exact measurement. the orange bar's color is #f28b82. the color of the grey bar behind it is #5f6368.  If the orange bar is  the same or bigger than the grey bar, display ">= 100%" for "Population: "

# The response should always be in the following format (replace [text] with the actual text in the image):
# Live: [text]
# Population: [population text]

# replace [text] with the actual text in the image
# replace [population text], can either be in the format of "X% less than usual" of the orange bar is smaller than the grey bar, or ">= 100%" if the orange bar is the same or bigger than the grey bar