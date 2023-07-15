import time
import os
import pandas as pd
import urllib
import argparse
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

parser = argparse.ArgumentParser()
parser.add_argument('--pages', help='how many times to extend car results for a page', type=int, default=9)
parser.add_argument('--groups', help='how many groups to divide states into', type=int, default=6)
parser.add_argument('--groupno', help='which number of group to scrape', type=int)

args = parser.parse_args()

if not args.groupno:
    print('Please specify a group to scrape using --groupno argument!')
    exit(0)

common_states = [
    "AL", "AZ", "AR", "CO", "CT", "DC", "DE", "FL", "GA", 
    "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
    "CA", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI",
]

SAVE_DIR = 'car_imgs/'
SUB_DIR = f'group{args.groupno}/'
METADATA_DIR = 'metadata/'
LOAD_MORE_TIMES = args.pages
GROUP_LEN = len(common_states) // args.groups

BASE_URL = 'https://www.carmax.com/cars/all'

list_images = list()
list_colors = list()
list_makes = list()
list_models = list()
list_years = list()

def next_page(driver, load_time=5):
    try:
        driver.find_elements(By.CSS_SELECTOR, '.see-more.see-more__cta-all > hzn-button')[0].click()
        time.sleep(load_time)
        return 1
    except:
        print('Load next page error!')
        return 0

def get_state_stores_count(driver, state_name):
    driver.find_element(By.ID, 'header-my-store-button').click()
    time.sleep(0.1)
    driver.find_element(By.ID, 'header-store-search-form-input').send_keys(state_name)
    time.sleep(0.1)
    driver.find_element(By.ID, 'header-store-search-button').click()
    time.sleep(3)
    stores = driver.find_elements(By.CSS_SELECTOR, 'li .store-chooser-modal_list-store-select > button')
    time.sleep(0.1)
    driver.find_element(By.CLASS_NAME, 'store-chooser-modal_header-close').click()
    time.sleep(0.1)
    driver.find_element(By.ID, 'header-my-store-button').click()
    time.sleep(0.1)
    driver.find_element(By.ID, 'header-store-search-form-input').clear()
    time.sleep(0.1)
    driver.find_element(By.XPATH, "//html").click()
    return len(stores) - 1

def change_store(driver, state_name, store_index, load_time=3):
    driver.find_element(By.ID, 'header-my-store-button').click()
    time.sleep(0.1)
    driver.find_element(By.ID, 'header-store-search-form-input').send_keys(state_name)
    time.sleep(0.1)
    driver.find_element(By.ID, 'header-store-search-button').click()
    time.sleep(3)
    stores = driver.find_elements(By.CSS_SELECTOR, 'li .store-chooser-modal_list-store-select > button')
    time.sleep(3)
    try:
        stores[store_index].click()
        time.sleep(load_time)
        print(f'Change to store {state_name} {store_index + 1}.')
        return 1
    except:
        print('Error changing to store!')
        driver.find_element(By.CLASS_NAME, 'store-chooser-modal_header-close').click()
        return 0

def get_color(car_id):
    url = 'https://www.carmax.com/car/' + car_id
    page = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"})
    soup = BeautifulSoup(page.text, 'html.parser')
    info = soup.select('.tombstone-badge')
    for i in info:
        if 'Color' in str(i):
            return i.text
    return 0

def create_dir():
    if SAVE_DIR[:-1] not in os.listdir():
        os.mkdir(SAVE_DIR)
    os.chdir(SAVE_DIR)
    if SUB_DIR[:-1] not in os.listdir():
        os.mkdir(SUB_DIR)
    os.chdir('..')
    if METADATA_DIR[:-1] not in os.listdir(SAVE_DIR):
        os.mkdir(SAVE_DIR + METADATA_DIR)

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    return webdriver.Chrome(options=options)

create_dir()
driver = get_driver()
driver.get(BASE_URL)

start_idx = (args.groupno - 1) * GROUP_LEN
end_idx = start_idx + GROUP_LEN

print(f'Starting group_{args.groupno}: {common_states[start_idx:end_idx]}...')

for state in common_states[start_idx:end_idx]:

    cnt = get_state_stores_count(driver, state)
    print(f'Found {cnt} stores in {state}')

    if cnt == 0:
        continue

    for i in range(cnt):
        
        store_status = change_store(driver, state, i)
        if not store_status:
            continue

        for j in range(LOAD_MORE_TIMES):
            print(f'Loading page {j+2}...')
            load_status = next_page(driver)
            if not load_status:
                break

        car_imgs = driver.find_elements(By.CSS_SELECTOR, '.sc--carousel-item.sc--hero-image img')
        car_year_makes = driver.find_elements(By.CLASS_NAME, 'sc--make-model-info--year-make')
        car_model_trims = driver.find_elements(By.CLASS_NAME, 'sc--make-model-info--model-trim')

        print(f'{len(car_imgs)} cars retrieved, start downloading...')

        for k, img in enumerate(car_imgs):
            try:
                src = img.get_attribute('src')
                car_id = src.split('/')[4]
                filename = car_id + '.jpg'
                color = get_color(car_id)
                if not color:
                    print('Get color error!')
                    raise Exception
                year = car_year_makes[k].text.split()[0]
                make = car_year_makes[k].text.split()[1]
                model = car_model_trims[k].text
                urllib.request.urlretrieve(src, SAVE_DIR + SUB_DIR + filename)

                list_images.append(filename)
                list_colors.append(color)
                list_years.append(year)
                list_makes.append(make)
                list_models.append(model)
            except:
                print('Get year/model/make error!')
                continue

df_meta = pd.DataFrame({
    'filename': list_images,
    'color': list_colors,
    'year': list_years,
    'make': list_makes,
    'model': list_models
})

df_meta.to_csv(SAVE_DIR + METADATA_DIR + f'metadata_group{args.groupno}.csv', index=False)

print(f'Total cars downloaded: {len(df_meta)}.')

driver.close()

print('Start sleeping for one day...')
time.sleep(86400)
