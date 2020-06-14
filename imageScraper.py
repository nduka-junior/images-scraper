PATH ="C:\Program Files (x86)\chromedriver.exe"
from selenium import webdriver
import requests
import time
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import re


# differnt user agent to avoid the notification
# of bots to google
options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')
driver = webdriver.Chrome(chrome_options=options, executable_path=PATH)


# what do you want to scrape
itemsToScrape = 'cat'


driver.get(f"https://www.pexels.com/search/{itemsToScrape}/")

# wait for page to load
time.sleep(10)

# scroll to the bottom of the page so more images will load

last_height = driver.execute_script("return document.body.scrollHeight")
i = 0
# the higher a number is greater than i the more images to be scraped
while i < 1000:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(5)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")
        break
    last_height = new_height
    i+=1
    print(i)
# find the images by class name
Images = driver.find_elements_by_class_name('photo-item__img')

imagesNumb = int(len(Images))

y = 0
# loop through the images
while y < imagesNumb:
    # ImagesAttrib grabs the attribute('data-big-src') from the image
    ImagesAttrib = Images[y].get_attribute('data-big-src')

    r = requests.get(ImagesAttrib)
    # check if the image has an extension of jpg,png,gif,or jpeg
    regex = r"\.jpeg|\.png|\.gif|\.jpg"
    imgName = re.search(regex, ImagesAttrib, re.MULTILINE).group()
    print(imgName)
    # download and store the image
    with open(f'{y}{imgName}', 'wb') as file:
        file.write(r.content)
    y+=1
# total length of images scaped
print(len(Images))
