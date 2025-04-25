from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import time


service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = ("https://mathscinet.ams.org/mathscinet/authors-search?query=")

with open("names.txt", "r") as f:
    names = f.read().splitlines()

df = []

def append_information() :
  official_name = driver.find_element(By.CSS_SELECTOR, ".author-title-margin > span:nth-child(1)")
  mr_author_id = driver.find_element(By.CSS_SELECTOR, "div.px-4:nth-child(1) > table:nth-child(1) > tr:nth-child(1) > td:nth-child(2)")
  earliest_indexed_publication = driver.find_element(By.CSS_SELECTOR, "div.px-4:nth-child(1) > table:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > a:nth-child(1)")
  total_publications = driver.find_element(By.CSS_SELECTOR, "div.px-4:nth-child(1) > table:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > a:nth-child(1)")

  try :
    total_related_publications = driver.find_element(By.CSS_SELECTOR, "div.px-4:nth-child(1) > table:nth-child(1) > tr:nth-child(4) > td:nth-child(2) > a:nth-child(1)")
  
  except :
    total_related_publications = driver.find_element(By.CSS_SELECTOR, "div.px-4:nth-child(1) > table:nth-child(1) > tr:nth-child(4) > td:nth-child(2) > div:nth-child(1)")

  try :
    total_reviews = driver.find_element(By.CSS_SELECTOR, "div.px-4:nth-child(1) > table:nth-child(1) > tr:nth-child(5) > td:nth-child(2) > a:nth-child(1)")
  
  except :
    total_reviews = driver.find_element(By.CSS_SELECTOR, "div.px-4:nth-child(1) > table:nth-child(1) > tr:nth-child(5) > td:nth-child(2) > span:nth-child(1)")

  try :
    total_citations = driver.find_element(By.CSS_SELECTOR, "div.px-4:nth-child(1) > table:nth-child(1) > tr:nth-child(6) > td:nth-child(2) > a:nth-child(1)")

  except:
    total_citations = driver.find_element(By.CSS_SELECTOR, "div.px-4:nth-child(1) > table:nth-child(1) > tr:nth-child(6) > td:nth-child(2) > div:nth-child(1)")
    
  unique_citing_authors = driver.find_element(By.CSS_SELECTOR, "div.px-4:nth-child(1) > table:nth-child(1) > tr:nth-child(7) > td:nth-child(2)")
  df.append([official_name.text, mr_author_id.text, earliest_indexed_publication.text, total_publications.text, total_related_publications.text, total_reviews.text, total_citations.text, unique_citing_authors.text])
  

for name in names :
  driver.get(url + name + "&size=100")

  time.sleep(2)

  if "authorId=" in driver.current_url :
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".author-title-margin > span:nth-child(1)")))
    append_information()


  else :
    elements = driver.find_elements(By.CSS_SELECTOR, "tr.results > td:nth-child(1) > a:nth-child(1)")
    multiple_urls = [element.get_attribute('href') for element in elements]
    for urls in multiple_urls :
      driver.get(urls)
      WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".author-title-margin > span:nth-child(1)")))
      append_information()



df = pd.DataFrame(df, columns=["Name", "MR Author ID", "Earliest Indexed Publication", "Total Publications",
                              "Total Related Publications", "Total Reviews", "Total Citations",
                              "Unique Citing Authors",])

df.set_index("Name", inplace=True)

df.to_csv("mathscinet-output.csv")
