import os
import sys

import logging
import gspreader.gspreader as gspreader
# from rivertils import sleep
from selenium.webdriver.common.by import By
from rich import print
import core.__main__ as core
from dotenv import load_dotenv
load_dotenv()
# from time import sleep
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
print("\nyoutubetakedown.py")
if "maintenance.py" in sys.argv:
    sys.argv=['youtubetakedown.py']


def sleep(seconds):
    """
    Sleep for a given number of seconds.
    """
    print(f"Sleeping for {seconds} seconds...")
    time.sleep(seconds)

description = """
    1.  gets video_ides from https://docs.google.com/spreadsheets/d/1ABCty-HQLNOH8ee0kolUIAuCgI_9xPyp0yVTJPljnRU/edit#gid=0
    2. uses selenium to issue takedown requests
    """
print(sys.argv)


logging.basicConfig(level=logging.INFO)

class YoutubeRequest:
    def __init__(self, video_id, date_preset, sheet_header):
        self.video_id = video_id
        self.date_preset = date_preset
        self.sheet_header = sheet_header
    
    def __repr__(self):
        return f"{self.video_id} {self.date_preset} {self.sheet_header}"


def login_to_googledoesntwork(email, password):
    CHROMEDRIVER_PATH = r"C:\RC Dropbox\Rivers Cuomo\Apps\chromedriver.exe"
    # # Set up the WebDriver
    # driver = webdriver.Chrome(executable_path="CHROMEDRIVER_PATH")
    # # driver = uc.Chrome()

    # Set up the WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = uc.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
    
    # Navigate to the Google login page
    driver.get("https://accounts.google.com/signin/v2/identifier")
    sleep(2)

    # Input the email and press ENTER
    # email_input = driver.find_element(by= '//*[@id="identifierId"]')
    core.wait_and_send_keys(driver, email, '//*[@id="identifierId"]')
    core.wait_and_send_keys(driver, Keys.RETURN, '//*[@id="identifierId"]')
    sleep(2)

    core.wait_and_send_keys(driver, password, '//*[@id="password"]/div[1]/div/div[1]/input')
    core.wait_and_send_keys(driver, Keys.RETURN, '//*[@id="password"]/div[1]/div/div[1]/input')
    sleep(2)

    # # Input the password and press ENTER
    # password_input = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
    # password_input.send_keys(password)
    # password_input.send_keys(Keys.RETURN)
    # sleep(2)

    # # If the login is successful, you'll be redirected to the Google homepage
    # print("Logged in as", driver.find_element_by_css_selector('#gb > div.gb_Wd.gb_nd.gb_od > div.gb_B.gb_C.gb_R.gb_md > div > a > span.gb_0.gb_4a.gb_5c').text)
    # driver.quit()


def google_sign_in(driver, url="https://studio.youtube.com/"):
    """ This doesn't work because google blocks it """
    username = os.environ.get("GOOGLE_EMAIL")
    password = os.environ.get("GOOGLE_PASSWORD")
    driver.get(url)
    
    

    email_x = '//*[@id="identifierId"]'
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, email_x))
    )
    email = driver.find_element(by=By.XPATH, value=email_x)
    email.send_keys(username)

    next_x = '//*[@id="identifierNext"]/div/button'
    email = driver.find_element(by=By.XPATH, value=next_x).click()

    password_x = ''
    pw = driver.find_element(by=By.XPATH, value=password_x)
    pw.send_keys(password)

    # login_button_xpath = r'//*[@id="login-button"]/div[1]'
    # lb_xpath = r'//*[@id="login-button"]/span[1]/span'
    driver.find_element(by=By.ID, value="login-button").click()

    sleep(1)  # rc


def sanitize(s:str):
    return s.lower().replace(" ", "")


def get_title(title: str):
    test = sanitize(title)
    return "Rivers Cuomo" if "rivers" in test else "Weezer"


def main():

    sheet = gspreader.get_sheet("youtube", 0)

    data = sheet.get_all_records()

    data = [x for x in data if x["takedown"] == ""]

    # driver = core.get_driver()
    driver = uc.Chrome()

    driver.delete_all_cookies()

    # google_sign_in(driver)    

    for row in data[:4]:

        video_id = row["video_id"]
        title = row["title"]
        artist = get_title(title)

        # # open the youtube page at the base url
        manual_claiming_url = "https://studio.youtube.com/owner/v44qCPasIFl9dXsTbbFiqg/claims/manual?o=v44qCPasIFl9dXsTbbFiqg&filter=%5B%5D&sort=%7B%22columnType%22%3A%22video%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D"

        # print(f"searching for {claim_url}")

        # open the youtube page at the base url
        driver.get(manual_claiming_url)

        # core.wait_and_send_keys(driver, os.environ["GOOGLE_EMAIL"], '//*[@id="identifierId"]')

        ## You'll have to manually sign in here
        sleep(25)
        
        print("Enter the video id into the search bar and hit enter...")
        enter_id = 'text-input'
        core.send_keys_and_click(driver, video_id, enter_id, by=By.ID)

        ids = [
            'video-title', # click on the video title
            "select-asset-button", # select asset 
            'create', # create asset     
            ]
        for i in ids:
            core.click(driver, i, by=By.ID)
            sleep(1)

        print("Locate the radio button element using its id...", end=" ")
        radio_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "global-radio-button")))

        # Click on the radio button to select it
        radio_button.click()
        print("done")

        # ids = [
        #     # 'trigger',  # click on select asset dropdown
            
        #     # 'create', 
        #     # 'offRadio', 
        #     # 'trigger', 
        #     # 'text-item-3'
        #     ]
        # for i in ids:
        #     core.click(driver, i, by=By.ID)
        #     sleep(2)



        # dropdown_trigger = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "ytcp-dropdown-trigger"))
        # )
        # driver.execute_script("arguments[0].scrollIntoView();", dropdown_trigger)

        # print("Now, wait for the overlay to disappear before clicking on the drop-down trigger:")


        # overlay = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "tp-yt-iron-overlay-backdrop"))
        # )
        # WebDriverWait(driver, 10).until_not(EC.visibility_of(overlay))

        # dropdown_trigger.click()
        print("Now, wait for the overlay to disappear before clicking on the drop-down trigger:", end=" ")
        blocking_element_locator = (By.CSS_SELECTOR, 'tp-yt-iron-overlay-backdrop.opened')
        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located(blocking_element_locator))
        print("done")

        # print("Click on the drop-down trigger to open the list of options:", end=" ")
        # element_locator = (By.ID, 'trigger')
        # element = driver.find_element(*element_locator)

        # driver.execute_script("arguments[0].click();", element)


        
        # sleep(3)
        # core.click(driver, "trigger", by=By.ID)
        # sleep(3)
        print("done")

        print("# 4. Select the 4th item (sound recording) from the list of options.")
        fourth_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#text-item-3 > ytcp-ve > div > div > yt-formatted-string"))
        )
        fourth_item.click()

        song_id = 'metadata-sound-recording-song-input'
        print(f'Song: {title}')
        core.send_keys_and_click(driver, title, song_id, by=By.ID)
        sleep(1)

        print(f'Artists: {artist}')
        artist_id = 'text-input'
        core.wait_and_send_keys(driver, artist, artist_id, by=By.ID)
        sleep(1)

        print('signature: Rivers Cuomo')
        # signature_x = '//*[@id="section-label"]'
        signature_id = 'section-label'
        signature_id = "manual-claim-takedown"
        core.wait_and_send_keys(driver, "Rivers Cuomo", signature_id, by=By.ID)
        sleep(1)


        print('acknowledgement checkbox')
        # acknowledgement_x = '//*[@id="acknowledge-checkbox"]/ytcp-checkbox-lit'
        acknowledgement_id = 'acknowledge-checkbox'
        core.click(driver, acknowledgement_id, by=By.ID)

        print('takedown button')
        takedown_x = '//*[@id="takedown-button"]/div'
        takedown_id = 'takedown-button'
        core.click(driver, takedown_id, by=By.ID)

        row["takedown"] = "x"
        
        sleep(5)

    
    driver.close()    

    gspreader.update_range(sheet, data)

    return "Success!"






if __name__ == "__main__":

    main()





# def build_requests():
#     base_url = "https://www.last.fm/music/Weezer/+tracks?"
#     date_presets = [
#        {"date_preset": "ALL", "sheet_header":"lastfm_all"},        
#         {"date_preset":"LAST_30_DAYS", "sheet_header":"lastfm_30_days"},       
#         {"date_preset":"LAST_365_DAYS", "sheet_header":"lastfm_365_days"}
#          # "LAST_7_DAYS",
#         # "LAST_90_DAYS",
#         # "LAST_180_DAYS",
#     ]

#     requests = []
#     for date_preset in date_presets:
#         for i in range(1, 11):
#             date= date_preset["date_preset"]
#             requests.append(YoutubeRequest(url=f"{base_url}date_preset={date}&page={i}", date_preset=date, sheet_header=date_preset["sheet_header"]))
#         # requests.extend(
#         #     f"{base_url}date_preset={date_preset}&page={i}"
            
#         # )
#     return requests


# def open_last_fm_page(driver, page):
#     print(f"\nopen_last_fm_page: {page}")
#     driver.get(page)
#     print("opened last.fm")


# def scrape_page(driver, request: YoutubeRequest, data, fromsongs=1, tosongs=53):
#     # data = [] # if you want to wipe out the sheet and start over

#     print(f"scrape_page from {fromsongs} to {tosongs}")

#     # search_link = "https://artists.spotify.com/c/artist/3jOstUTkEu2JkjvRdBA5Gu/catalog/released/songs"

#     # driver.get(search_link)

#     for i in range(int(fromsongs), int(tosongs) + 1):

#         print(f"{i}", end=": ")
#         i = str(i)

#         table_rowx = f'//*[@id="mantle_skin"]/div[3]/div[2]/div[1]/section[1]/div[2]/table/tbody/tr[{i}]'

#         core.wait_for_element(driver, table_rowx)

#         elem = driver.find_element(by=By.XPATH, value=table_rowx)
#         text = elem.text # '1 Play track\nLove this track\nBuddy Holly\n1,380,948 listeners'
#         elems = text.split("\n") # ['1 Play track', 'Love this track', 'Buddy Holly', '1,380,948 listeners']
#         if len(elems) < 4:
#             print(f"skipping {i} because it's not a song")
#             print(text)
#             print(elems)
#             continue
#         title = str(elems[2])
#         print(title)
#         listeners = elems[3].split(" ")[0].replace(",", "")
#         data.append({"song_title": title, request.sheet_header: listeners})

#         # if row := next(
#         #     (x for x in data if gspreader.sanitize_key(str(x["song_title"])) == gspreader.sanitize_key(title)),
#         #     None,
#         # ):
#         #     row[data_date_range]=listeners
#         # else:
#         #     print(f"couldn't find {title} in sheet")
#         #     # if "All My Favorite Songs (feat. AJR)"==title:
#         #     data.append({"song_title": title, data_date_range: listeners})

#     return data

