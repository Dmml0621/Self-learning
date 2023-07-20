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
parser.add_argument('--pages', help='how many times to extend clothes results for a page', type=int, default=3)

args = parser.parse_args()

LOAD_MORE_TIMES = args.pages
SAVE_DIR = 'clothes_imgs/'
# SUB_DIR = f'??/'
METADATA_DIR = 'metadata/'
genders = ['Female', 'Male']

BASE_URL = 'https://www.nordstrom.com/?origin=tab-logo'

list_images = list()
list_colors = list()

def next_page(driver, load_time=3):
    prev_next_buttons = driver.find_elements(By.CLASS_NAME, 'dtuHL')
    if len(prev_next_buttons) == 1:
        prev_next_buttons[0].click()
    else:
        prev_next_buttons[1].click()
    time.sleep(load_time)

def get_categories_and_count(driver, gender):
    if gender == 'Male':
        driver.find_element(By.ID, 'flyout-anchor-index-control-2').click()
    else:
        driver.find_element(By.ID, 'flyout-anchor-index-control-1').click()
    time.sleep(0.1)
    category_list = driver.find_elements(By.CSS_SELECTOR, '.L9PTf:nth-child(2) > li > a')
    categories = [cl.get_attribute("innerHTML") for cl in category_list]
    driver.find_elements(By.CLASS_NAME, 'nui-icon-large-clear-0')[-1].click()
    return categories, len(category_list)

def change_category(driver, gender, index):
    if gender == 'Male':
        driver.find_element(By.ID, 'flyout-anchor-index-control-2').click()
    else:
        driver.find_element(By.ID, 'flyout-anchor-index-control-1').click()
    time.sleep(1)
    driver.find_elements(By.CSS_SELECTOR, '.L9PTf:nth-child(2) > li > a')[index].click()
    time.sleep(5)

def get_colors_and_count(driver):
    driver.find_element(By.ID, 'color-heading').click()
    time.sleep(0.1)
    color_list = driver.find_elements(By.CSS_SELECTOR, '#color-panel > div > label > a')
    colors = [cl.get_attribute("innerHTML") for cl in color_list]
    return colors, len(color_list)

def change_color(driver, index):
    driver.find_elements(By.CSS_SELECTOR, '#color-panel > div > label > a')[index].click()
    time.sleep(3)

def create_dir():
    if SAVE_DIR[:-1] not in os.listdir():
        os.mkdir(SAVE_DIR)
    if METADATA_DIR[:-1] not in os.listdir(SAVE_DIR):
        os.mkdir(SAVE_DIR + METADATA_DIR)

def get_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--no-sandbox')
    # options.add_argument('--headless=new')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--window-size=1920,1080')
    # options.add_argument('--start-maximized')
    return webdriver.Chrome(options=options)

create_dir()
driver = get_driver()
driver.get(BASE_URL)

time.sleep(2)

for gender in genders[:1]:

    categories, category_cnt = get_categories_and_count(driver, gender)
    time.sleep(3)

    for i, category in enumerate(categories[:2]):

        change_category(driver, gender, i)

        colors, colors_count = get_colors_and_count(driver)
        time.sleep(3)

        for j, color in enumerate(colors[:2]):
            change_color(driver, j)
            
            print(f'Downloading {gender} {color} {category}...')

            for k in range(LOAD_MORE_TIMES):
                image_articles = driver.find_elements(By.CSS_SELECTOR, '.DSQCI.TLihj article')
                for ia in image_articles:
                    try:
                        if ia.find_element(By.TAG_NAME, 'span').get_attribute == 'Sponsored':
                            print('Sponsored result found!')
                    except:
                        src = ia.find_element(By.TAG_NAME, 'img').get_attribute('src')
                        filename = src.split('/')[5].split('?')[0]
                        urllib.request.urlretrieve(src, SAVE_DIR + filename)

                        list_images.append(filename)
                        list_colors.append(color)
                    
                time.sleep(0.1)
                try:
                    next_page(driver)
                except:
                    print('Reach end of the results!')
                    break

            time.sleep(3)

        time.sleep(3)
    
    time.sleep(5)

df_meta = pd.DataFrame({
    'filename': list_images,
    'color': list_colors
})

df_meta.to_csv(SAVE_DIR + METADATA_DIR + f'metadata.csv', index=False)

driver.close()

# print('Start sleeping for one day...')
# time.sleep(86400)