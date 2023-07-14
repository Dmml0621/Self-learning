import json
import time
import os
from datetime import datetime
from urllib.parse import unquote
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By


url_login = "https://auth.ecobee.com/u/login?state=hKFo2SA3N0FyTVo0cXdBOV92aEZoNXE2bUZpcjEyQklxWGlucKFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIDRNcUlXNXNmWVN4QTMyUGFEdDgtaTBrbkt4NTRKalZMo2NpZNkgMTgzZU9SRlBsWHl6OUJiRFp3cWV4SFBCUW9WamdhZGg"
url_dl_1 = "https://www.ecobee.com/consumerportal/index.html#/devices/thermostats/"
url_dl_2 = "/homeiq/diagnostics/downloadData"


def ecobee_login(username: str, password: str, load_time=8) -> webdriver.Chrome:
    dc = DesiredCapabilities.CHROME
    dc['goog:loggingPrefs'] = {'performance': 'ALL'}
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(desired_capabilities=dc, options=options)
    print(f"Logging into {username}...")
    driver.get(url_login)
    driver.find_element("id", "username").send_keys(username)
    driver.find_element("id", "password").send_keys(password)
    login_button = driver.find_elements(By.TAG_NAME, "button")[-1]
    login_button.click()
    time.sleep(load_time)
    print("Login success!")
    return driver

def ecobee_logout(driver: webdriver.Chrome) -> None:
    driver.quit()

def convert_date(date: datetime) -> str:
    month_to_word = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }
    return f"{month_to_word[date.month]}-{date.year}-{date.day}"

def get_device_ids(driver: webdriver.Chrome) -> list:
    logs = driver.get_log("performance")
    device_list = None

    for log in logs:
        response = json.loads(log["message"])["message"]
        try:
            p = response["params"]["request"]
            if "thermostatSummary" in p["url"]:
                parsed = (p["url"].split("&")[1]).replace("json=", "")
                devices = json.loads(unquote(parsed))['selection']['selectionMatch']
                device_list = devices.split(",")
                time.sleep(0.1)
                print("Get devices success!")
                break
        except:
            pass
    
    if device_list == device_list:
        return device_list
    else:
        print("Error getting devices!")
        return None
    
def download_data(driver: webdriver.Chrome, mode: str, start_time, end_time) -> None:
    buttons = driver.find_elements(By.TAG_NAME, "button")
    if mode == '1':
        buttons[0].click()
    elif mode == '2':
        buttons[1].click()
    else:
        arrow_right = driver.find_elements(By.CSS_SELECTOR, "div.calendar__arrow-previous")[1]
        time.sleep(.1)
        skip_to_month(arrow_right, end_time)
        time.sleep(.1)
        driver.find_elements("id", convert_date(end_time))[1].click()
        time.sleep(.1)
        if start_time.month != end_time.month:
            driver.find_elements(By.CSS_SELECTOR, "div.calendar__arrow-previous")[0].click()
            time.sleep(.1)
        driver.find_elements("id", convert_date(start_date))[0].click()
        time.sleep(.1)
        buttons[2].click()

    time.sleep(3)

def check_gap(start_date: datetime, end_date: datetime) -> bool:
    if start_date > datetime.now() or end_date > datetime.now():
        print("Cannot use a future date.")
        return False
    if (end_date - start_date).days <= 31:
        return True
    else:
        print("Maximum range should not exceed 31 days.")
        return False

def skip_to_month(button, end, wait_time=.1):
    now = datetime.now()
    diff_month = (now.year - end.year) * 12 + now.month - end.month
    for i in range(diff_month):
        button.click()
        time.sleep(wait_time)

def download_account(account: tuple) -> None:
    print(f"Scrapping account: {account[0]}")
    driver = ecobee_login(account[0], account[1])
    device_list = get_device_ids(driver)
    if device_list != device_list:
        print("Exiting program...")
        exit(0)
    
    for device in device_list:
        print(f"Downloading for device: {device}")
        link = url_dl_1 + device + url_dl_2
        driver.get(link)
        time.sleep(1)
        driver.refresh()
        time.sleep(10)
        download_data(driver, mode, start_date, end_date)
        print(f"Files downloaded for device: {device}")
        for f in os.listdir(f"{os.path.expanduser('~')}/Downloads"):
            if f.startswith(f"report-{device}"):
                print(f"~/Downloads/{f}")

    ecobee_logout(driver)

if __name__ == "__main__":
    print("Welcome to the Ecobee scraping program!")
    print("1. Today's data")
    print("2. Last 7 day's data")
    print("3. Customize date range")

    while True:
        mode = input("Please enter number for scraping option: ")
        if mode in ["1", "2", "3"]:
            break

    start_date = None
    end_date = None

    if mode == '3':
        while True:
            start_date = input("Enter start date (Y/M/D): ")
            end_date = input("Enter end date (Y/M/D): ")

            if start_date == "" or end_date == "":
                continue

            start_date = datetime.strptime(start_date, "%Y/%m/%d")
            end_date = datetime.strptime(end_date, "%Y/%m/%d")

            if check_gap(start_date, end_date):
                break
    
    accounts = [
        ("hwj-study1@umich.edu", "heatingwithjusticedata"),
        ("hwj-study@umich.edu", "heatingwithjusticedata"),
        ("clairejm@umich.edu", "heatingwithjusticedata")
    ]

    print("Account list")

    for i, acc in enumerate(accounts):
        print(f"{i}: {acc[0]}")

    acc_choice = input("Choose an account to scrape, press enter to scrape all: ")

    if acc_choice == "":
        accounts_selected = accounts
    else:
        accounts_selected = [accounts[int(acc_choice)]]

    for account in accounts_selected:
        download_account(account)
    
    print("Scraping process done!")
