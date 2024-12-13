from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    ElementNotInteractableException,
    NoSuchWindowException,
)
import time
import json
import os
import streamlit as st


def scrapData(urlLink):
    if urlLink == "":
        return
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(urlLink)
    # Extracting restaurant name 
    try:
        restName = driver.find_element(By.CLASS_NAME, 'E-vwXONV9nc-').text
        file_path = os.path.join("F:\Virtual Environment\python",f'{restName}.json')
        if os.path.isfile(file_path):
            st.write(f"Scrapping of {restName} Restaurant is already done")
            driver.quit()
            return restName
        else:
            st.write(f"The file '{restName}.json' is not present in the folder. We have to wait for the reviews to be scrapped")
    except NoSuchElementException:
        print("No Restaurant found on the page.")
        return None

    reviewsStore = {}
    i = 0
    while True:
        try:
            # Waiting for reviews to load
            time.sleep(2)
            # Locating reviews on the page
            reviewsList = driver.find_elements(By.CLASS_NAME, 'afkKaa-4T28-')
            # case when the issue is try refreshing the webpage
            if not reviewsList:
                print("No reviews found. Refreshing the page...")
                driver.refresh()
                time.sleep(2)
                continue
            elif reviewsList:
                # Scrape each review
                for reviewDiv in reviewsList:
                    try:
                        temp = {}
                        # extracting data and time
                        temp['Date'] = reviewDiv.find_element(By.CLASS_NAME, 'iLkEeQbexGs-').text.replace("Dined on ", "").replace("Dined ","")
                        temp['Review'] = reviewDiv.find_element(By.CLASS_NAME, '_6rFG6U7PA6M-').text.replace("Read more", "").replace('\n', "")
                        
                        # Collecting ratings
                        reviews = reviewDiv.find_elements(By.CLASS_NAME, '-k5xpTfSXac-')
                        for review in reviews:
                            try:
                                reviewType, rating = review.text.split(' ')
                                temp[reviewType] = rating
                            except ValueError:
                                print(f"Error parsing review text: {review.text}")
                        
                        reviewsStore[f"Review{i}"] = temp
                        i += 1                
                    except NoSuchElementException as e:
                        print(f"Error extracting review details: {e}")

            elif len(reviewsList) == 0:
                print("Maximum reviews have been scrapped")
                break
            # clicking next button
            try:
                nextButton = driver.find_element(By.XPATH,"//a[@aria-label='Go to the next page']")
                nextButton.click()
            except (StaleElementReferenceException, ElementClickInterceptedException) as e:
                print(f"Error clicking on Next button: {e}. Retrying...")
                time.sleep(2)
                # next_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[2]/div[1]/section[7]/section/footer/div/div[2]/a')
                # next_button.click()
                nextButton = driver.find_element(By.XPATH,"//a[@aria-label='Go to the next page']")
                nextButton.click()
            print(f"Next page pressed: {restName}")
        except (NoSuchElementException, ElementNotInteractableException, NoSuchWindowException) as e:
            print(f"Breaking loop due to exception: {e}")
            break

    with open(f"{restName}.json",'w') as file:
        json.dump(reviewsStore,file,indent= 5)
    driver.quit()
    return restName




scrapData("")