
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from dotenv import load_dotenv
import logging
import os
load_dotenv()



# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    try:
        logger.info("Attempting to set up Chrome driver...")
        
        # This line downloads and returns the path to the chromedriver binary
        service_path = ChromeDriverManager().install()
        
        # Ensure the chromedriver binary exists and is executable
        if not os.path.exists(service_path):
            logger.error(f"Chromedriver not found at path: {service_path}")
            raise OSError(f"Chromedriver not found at path: {service_path}")
        
        logger.info(f"Chromedriver path: {service_path}")
        
        service = ChromeService(service_path)
        driver = webdriver.Chrome(service=service, options=options)
        
        logger.info("Chrome driver set up successfully.")
        return driver
    except OSError as os_err:
        logger.error(f"OSError: {os_err.strerror}")
        raise os_err
    except Exception as e:
        logger.error(f"An error occurred while setting up the Chrome driver: {str(e)}")
        raise
# def get_driver():
#     options = Options()
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
    
#     try:
#         logger.info("Attempting to set up Chrome driver...")
#         service = ChromeService(ChromeDriverManager().install())
#         driver = webdriver.Chrome(service=service, options=options)
#         logger.info("Chrome driver set up successfully.")
#         return driver
#     except Exception as e:
#         logger.error(f"An error occurred while setting up the Chrome driver: {str(e)}")
#         raise


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




def click(driver, id, timeout=20, by=By.XPATH):
    # print('wait_and_click', id)
    print(f"click {id} by {by}...", end=" ")
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, id))
    ).click()
    print("done\n")


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

# Use the function
try:
    driver = get_driver()
    # Your code using the driver goes here
finally:
    if 'driver' in locals():
        driver.quit()
def log(item: dict):
    print(f" - {item['name']} {item['xpath']}")

# def get_driver():
#     options = webdriver.ChromeOptions()
#     options.add_argument("--ignore-certificate-errors")
#     options.add_argument("--ignore-ssl-errors")

#     options.add_experimental_option("excludeSwitches", ["enable-logging"])

#     # dir_path = os.path.dirname(os.path.realpath(__file__))
#     # chromedriver = f"{dir_path}/chromedriver"
#     # os.environ["webdriver.chrome.driver"] = chromedriver
#     try:
#         # driver = webdriver.Chrome(options=options)
#         driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(driver_version="latest").install()), options=options)
#     except Exception as e:
#         print(e.msg)
#         return e.msg
#     driver.set_window_size(1368, 786)
#     return driver


def send_keys_and_click(driver, text, id, by=By.XPATH):
    print(f'send_keys {text} and_click {id} by {by}', end=" ")
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((by, id))
            )
    
        keyword = driver.find_element(by=by, value=id)
        keyword.send_keys(text)
        keyword.send_keys(Keys.ENTER)
        print("done\n")
    except Exception as e:
        print(e)
        time.sleep(2)


def wait_and_click(driver, item, timeout=20, by=By.XPATH):
    print('wait_and_click', item)
    try:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, item["xpath"]))
        ).click()
    except Exception as e:
        print(e)
        time.sleep(2)

    
def wait_and_click_v2(driver,  id, timeout=20, by=By.XPATH):
    print(f'wait_and_click_v2 {id} {timeout}...', end=" ")
    wait = WebDriverWait(driver, timeout)
    try:
        element = wait.until(EC.element_to_be_clickable((by, id)))
        try:
            print("clicking", end="...")
            element.click()
            print("done\n")
        except Exception as e:
            print(e)
            time.sleep(4)
    except Exception as e:
        print(e)
        time.sleep(4)




# def click_id(driver, id, timeout=20, by=By.XPATH):
#     print('wait_and_click', id)
#     WebDriverWait(driver, timeout).until(
#         EC.presence_of_element_located((By.id, id))
#     ).click()


def wait_and_send_keys(driver, text, id, by=By.XPATH, timeout=20):
    print(f"wait_and_send_keys: '{text}' id", end=" ")
    wait = WebDriverWait(driver, timeout)
    
    try:
        element = wait.until(EC.element_to_be_clickable((by, id)))
        try:
            print("clicking", end="...")
            element.click()
            try:
                print("sending keys...", end=" ")
                element.send_keys(text)
                print("done\n")
            except Exception as e:
                print(e)
                time.sleep(2)
        except Exception as e:
            print(e)
            time.sleep(2)
    except Exception as e:
        print(e)
        time.sleep(2)

def wait_click_and_send_keys(driver, text, id, by=By.XPATH, timeout=20):
    print(f'wait_click_and_send_keys {text} {id}...', end=" ")
    wait = WebDriverWait(driver, timeout)
    
    try:
        element = wait.until(EC.element_to_be_clickable((by, id)))
        try:
            print("clicking", end="...")
            element.click()
            try:
                print("sending keys", end="...")
                element.send_keys(text)
                print("done\n")
            except Exception as e:
                print(e)
                time.sleep(2)
        except Exception as e:
            print(e)
            time.sleep(2)
    
    except Exception as e:
        print(e)
        time.sleep(2)
    
    # WebDriverWait(driver, 20).until(
    #     EC.presence_of_element_located((by, id))
    #     )
    # keyword = driver.find_element(by=by, value=id)
    # time.sleep(1)
    # keyword.click()
    # time.sleep(1)
    # keyword.click()
    # time.sleep(10)
    # keyword.send_keys(text)

    # attempts = 0
    # max_attempts = 3

    # while attempts < max_attempts:
    #     try:
    #         wait = WebDriverWait(driver, timeout)
    #         element = wait.until(EC.element_to_be_clickable((By.ID, id)))
    #         element.click()
    #         element.send_keys(text)
    #         break
    #     except StaleElementReferenceException:
    #         attempts += 1
    #         if attempts >= max_attempts:
    #             raise

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


def main():
    get_driver()

if __name__ == "__main__":
    main()

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
    # "Japan",
    # # "Germany",
    # # "Czech Republic",
    "France",
    "Spain",
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
