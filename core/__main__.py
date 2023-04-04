
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
from dotenv import load_dotenv
load_dotenv()

def consolidate_alt_versions_special(data):
    """
    "All My Favorite Songs" and "All My Favorite Songs feat. AJR"
    """
    print("consolidate_alt_versions_special...")

    ajr_index = data.index([x for x in data if "feat. AJR" in str(x["song_title"])][0])
    ajr = data.pop(ajr_index)
    all_my_fav = [x for x in data if "All My Favorite Songs" in str(x["song_title"])][0]

    if "saves_last_28_days" in ajr:
        all_my_fav["saves_last_28_days"] = str(int(all_my_fav["saves_last_28_days"]) + int(ajr["saves_last_28_days"]))

    if "streams_last_28_days" in ajr:
        all_my_fav["streams_last_28_days"] = str(int(all_my_fav["streams_last_28_days"]) + int(ajr["streams_last_28_days"]))

    if "streams_since_2015" in ajr:
        all_my_fav["streams_since_2015"] = str(int(all_my_fav["streams_since_2015"]) + int(ajr["streams_since_2015"]))

    if "lastfm_all" in ajr:
        all_my_fav["lastfm_all"] = str(int(all_my_fav["lastfm_all"]) + int(ajr["lastfm_all"]))

    if "lastfm_365_days" in ajr:
        all_my_fav["lastfm_365_days"] = str(int(all_my_fav["lastfm_365_days"]) + int(ajr["lastfm_365_days"]))

    if "lastfm_30_days" in ajr:
        all_my_fav["lastfm_30_days"] = str(int(all_my_fav["lastfm_30_days"]) + int(ajr["lastfm_30_days"]))

    return data

def log(item: dict):
    print(f" - {item['name']} {item['xpath']}")

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


def send_keys_and_click(driver, text, id, by=By.XPATH):
    print(f'send_keys {text} and_click {id} by {by}', end=" ")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((by, id))
        )
    keyword = driver.find_element(by=by, value=id)
    keyword.send_keys(text)
    keyword.send_keys(Keys.ENTER)
    print("done")


def wait_and_click(driver, item, timeout=20, by=By.XPATH):
    print('wait_and_click', item)
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, item["xpath"]))
    ).click()


def click(driver, id, timeout=20, by=By.XPATH):
    # print('wait_and_click', id)
    print(f"click {id} by {by}...", end=" ")
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, id))
    ).click()
    print("done")

# def click_id(driver, id, timeout=20, by=By.XPATH):
#     print('wait_and_click', id)
#     WebDriverWait(driver, timeout).until(
#         EC.presence_of_element_located((By.id, id))
#     ).click()

def wait_and_send_keys(driver, text, id, by=By.XPATH):
    print('wait_and_send_keys', text, id)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((by, id))
        )
    keyword = driver.find_element(by=by, value=id)
    keyword.send_keys(text)

def wait_for_element(driver, id, by=By.XPATH, timeout=20):
    # print(value, by, timeout)
    # THIS was timing out so I'm wrapping it in try
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, id))
        )
    except Exception as e:
        print(e)
        print(f"Waited for {timeout} but couldn't find '{id }' by {by} in page")


# def sanitize(s: str):
#     s = s.lower()
#     bads = ["'", '"', "(", ")", ":", ";", "!", "?", "’", "“", "”", "‘", "–", "—", "…", ",", ".", " ", "-"]
#     for b in bads:
#         s = s.replace(b, "")
#     return s


# def update_sheet_data(sheet_data: list, new_data: list, key: str):
#     """ update the sheet_data with the new_data (if there's a matching row in the new data)"""
#     print("update_sheet_data...")
#     for row in sheet_data:
#         for new_row in new_data:
#             if sanitize(str(row[key])) == sanitize(str(new_row[key])):
#                 # print(f"Updating {row[key]}")

#                 # Update the columns for this song in this new_row
#                 row.update(new_row)
#     return sheet_data

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
