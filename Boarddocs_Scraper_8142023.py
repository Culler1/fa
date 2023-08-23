import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import requests
import re
import datetime

# Read in the main database of boarddocs links. I had to divide the main list into sets of 50.
# This scraper will go through 50 districts in about 24 hours. I just copied this code into 9 notebooks and ran each one 
# at the same time. Just change a1[101:150] to any range you prefer or just cut that line entirely. 
a1 = pd.read_csv("school_mainPA.csv")
a1 = a1[101:150]
#these are the keywords we were looking for
keywords = ["sexuality",'at birth','male puberty','Biological','Critical race theory',
            'Partisan','Political','Indoctrination','Advocacy','Flag','Social policy','Race',
            'Racial','Controversial','Profanity','Sexual conduct','Graphic violence','Age-inappropriate',
            'Age-appropriate','Sexual acts','Sexualized','Nudity','LGBTQ','Gender ideology','sex assigned at birth',
            '3101','6312(g)','Implied depictions of sexual acts',
            'Partisan, Political, or Social Policy Advocacy', 'Neutrality']

# DataFrame to store the extracted data
extracted_data = pd.DataFrame(columns=['School District', 'County', 'URL', 'Text Content', 'Keywords Found', 'Number of Keywords Found'])

# Get the current date for file naming
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Loop through each row in the DataFrame
# the first try is checking the base policies boarddocs page for each district. It then collects 
# the unique IDs for each policy and then we use Beautiful Soup to scrape those new urls.
# If it finds the keyword in the policy text, it adds it to our database. 
for index, row in a1.iterrows():
    district = row['school_dis']
    county = row['cty_name']
    url = row['base_link']

    try:
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(1)
        element = driver.find_element(By.LINK_TEXT, "POLICIES")
        driver.execute_script('arguments[0].click()', element)
        time.sleep(5)
        soup_outer = BeautifulSoup(driver.page_source, "html.parser")
        href_elements = soup_outer.findChildren(attrs={'href': '#', 'unique': True})
        unique_values = [element.get("unique") for element in href_elements]
        time.sleep(2)
        for unique_value in unique_values:
            new_url = row['prePolicyID'] + unique_value
            try:
                response = requests.get(new_url)
                response.raise_for_status()  # Raise an exception if the response status code is not 200

                time.sleep(5)
                soup_inner = BeautifulSoup(response.content, "html.parser")
                container_div = soup_inner.find('div', id='policy-content')
                if container_div is not None:
                    text_content = container_div.get_text(" ", strip=True)
                    found_keywords = [keyword for keyword in keywords if re.search(r'\b{}\b'.format(re.escape(keyword)), text_content, re.IGNORECASE)]
                    if found_keywords:
                        for keyword in found_keywords:
                            text_content = re.sub(r'\b({})\b'.format(re.escape(keyword)), r'<b>\1</b>', text_content, flags=re.IGNORECASE)
                        extracted_data = extracted_data.append({'School District': district,
                                                                'County': county,
                                                                'URL': new_url,
                                                                'Text Content': text_content,
                                                                'Keywords Found': found_keywords,
                                                                'Number of Keywords Found': len(found_keywords)}, ignore_index=True)
                else:
                    print("Container div not found for", new_url)
            except Exception as e:
                # Handle any exception. If the error would cause the program to stop running, it will first
                # print a dataframe of what it has so far. 
                print(f"Exception occurred: {str(e)}. Saving current data to CSV...")
                extracted_data.to_csv('extracted_data_crashed.csv', index=False)
                print("Data saved. Script crashed.")
            
            except requests.exceptions.RequestException as e:
                # This is in case there's something wrong with the policy urls. It prints a warning and moves on.
                print(f"Failed to fetch data from {new_url}: {str(e)}")
            
            except KeyboardInterrupt:
                # Handle KeyboardInterrupt (Ctrl + C). It will print what it has so far to a datarframe.
                print("KeyboardInterrupt detected. Saving current data to CSV...")
                extracted_data.to_csv('extracted_data_interrupted.csv', index=False)
                print("Data saved. Script interrupted.")

            time.sleep(2)
# If it can't find the "policies" tab on the site, it'll print an error message with the URL that didn't work and move on
# to the next URL
    except Exception as e:
        print(f"Exception occurred for base URL {url}: {str(e)}")

    finally:
        driver.quit()

# Save the extracted data to a CSV file
csv_filename = f"policy3_extracted_data_{current_date}.csv"
extracted_data.to_csv(csv_filename, index=False)
print(f"Extracted data saved to {csv_filename}")
