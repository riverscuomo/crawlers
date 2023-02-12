
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
load_dotenv()


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")

    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    dir_path = os.path.dirname(os.path.realpath(__file__))
    chromedriver = f"{dir_path}/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1368, 786)
    return driver


def sanitize(s: str):
    s = s.lower()
    bads = ["'", '"', "(", ")", ":", ";", "!", "?", "’", "“", "”", "‘", "–", "—", "…", ",", ".", " ", "-"]
    for b in bads:
        s = s.replace(b, "")
    return s


def update_sheet_data(sheet_data: list, new_data: list, key: str):
    """ update the sheet_data with the new_data (if there's a matching row in the new data)"""
    print("update_sheet_data...")
    for row in sheet_data:
        for new_row in new_data:
            if sanitize(str(row[key])) == sanitize(str(new_row[key])):

                # Update the columns for this song in this new_row
                row.update(new_row)
    return sheet_data


def wait_for_element(driver, by, value):
    timeout = 20
    # THIS was timing out so I'm wrapping it in try
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, value))
        )
    except Exception:
        print(f"Waited for {timeout} but couldn't find xPath '{value}' in page")


countries_of_interest = [
    "United States",
    # "United Kingdom",
    # "Ireland",
    "Japan",
    # # "Germany",
    # # "Czech Republic",
    # "France",
    # "Spain",
    # "Italy",
    # "Indonesia",
    # "Netherlands",
    # "Belgium",
    # "Denmark",
    # "Sweden",
    # "Norway",
    # "Austria",
    # "Australia",
    # "Canada",
    # "New Zealand",
    # "Switzerland",
    # "Finland",
    # "Scotland", # not in Spotify
    # "England", # not in Spotify
]
