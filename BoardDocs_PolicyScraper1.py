import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import requests

# Read in the main database
a1 = pd.read_csv("school_mainPA.csv")

# For testing purposes, we're only going to be scraping a couple of these districts. 
a1 = a1.sample(3)

# Open the chrome driver
driver = webdriver.Chrome()

# List of keywords to check in the page content
keywords = ['The policies and procedures adopted by the Board establish the general parameters']
# keywords = ["sexuality",'at birth','Gender','sex','at birth','male puberty','Biological','Critical race theory',
#             'Partisan','Political','Indoctrination','Advocacy','Flag','Social policy','Race',
#             'Racial','Controversial','Profanity','Sexual conduct','Graphic violence','Age-inappropriate',
#             'Age-appropriate','Sexual acts','Sexualized','Nudity','LGBTQ','Gender ideology','sex assigned at birth',
#             '3101','6312(g)','Implied depictions of sexual acts',
#             'Partisan, Political, or Social Policy Advocacy', 'Neutrality']

# URL of the website
for index, row in a1.iterrows():
    url = row['base_link']
    print(url)
    driver.get(url)
    time.sleep(1)
    element = driver.find_element(By.LINK_TEXT, "POLICIES")
    driver.execute_script('arguments[0].click()', element)
    time.sleep(5)
    soup_outer = BeautifulSoup(driver.page_source, "html.parser")
    href_elements = soup_outer.findChildren(attrs={'href': '#', 'unique': True})
    unique_values = [element.get("unique") for element in href_elements]
    print(unique_values)
    time.sleep(2)
    for unique_value in unique_values:
        new_url = row['prePolicyID'] + unique_value
        response = requests.get(new_url)
        if response.status_code == 200:
            time.sleep(5)
            soup_inner = BeautifulSoup(response.content, "html.parser")
            container_div = soup_inner.find('div', id='policy-content')
            if container_div is not None:
                print(new_url)
                text_content = container_div.get_text(" ", strip=True).lower()  # Convert to lowercase
                # Convert keywords to lowercase and check if any of them are present in the text_content
                if any(keyword.lower() in text_content for keyword in keywords):
                    print(text_content)
            else:
                print("Container div not found for", new_url)
        else:
            print("Failed to fetch data from", new_url)

        time.sleep(2)
# Close the browser after the loop is done
driver.quit()
# ... (previous code)
