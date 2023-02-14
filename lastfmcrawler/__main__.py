import sys
import logging

from gspreader.gspreader import get_sheet, update_range

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import datetime
# import os
# import time
from rich import print
from rivertils import *
import core.__main__ as core
import core.scripts.my_args as my_args 
from dotenv import load_dotenv
load_dotenv()

print("\nlastfmcrawler.py")

# sheet = get_sheet("")
description = """
    1. updates the 'all' sheet in the 'Weezer Data' spreadsheet  
    with latest data from lastfm./weezer

    Currently matches with song_title in the sheet
    """

if "maintenance.py" in sys.argv:
    sys.argv=['lastfmcrawler.py']

args = my_args.get_args(description)

method = args.method

sys.path.insert(0, "C:\RC Dropbox\Rivers Cuomo\Apps")
logging.basicConfig(level=logging.INFO)

pages = [
    "https://www.last.fm/music/Weezer/+tracks?date_preset=ALL",
#     "https://www.last.fm/music/Weezer/+tracks?date_preset=LAST_7_DAYS",
    "https://www.last.fm/music/Weezer/+tracks?date_preset=LAST_30_DAYS",
#     "https://www.last.fm/music/Weezer/+tracks?date_preset=LAST_90_DAYS",
#     "https://www.last.fm/music/Weezer/+tracks?date_preset=LAST_180_DAYS",
    "https://www.last.fm/music/Weezer/+tracks?date_preset=LAST_365_DAYS",

]

ranges = [
    "lastfm_all",	
    # "lastfm_7_days"	,
    "lastfm_30_days"	,
    # "lastfm_90_days"	,
    # "lastfm_180_days",	
    "lastfm_365_days",
]

def open_last_fm_page(driver, page):
    print(f"\nopen_last_fm_page: {page}")
    driver.get(page)
    print("opened last.fm")

def scrape_page(driver, data, data_date_range, fromsongs=1, tosongs=53):
    # data = [] # if you want to wipe out the sheet and start over

    print(f"scrape_page from {fromsongs} to {tosongs}")

    # search_link = "https://artists.spotify.com/c/artist/3jOstUTkEu2JkjvRdBA5Gu/catalog/released/songs"

    # driver.get(search_link)

    for b in range(int(fromsongs), int(tosongs) + 1):

        print(f"{b}", end=": ")
        b = str(b)

        table_rowx = f'//*[@id="mantle_skin"]/div[3]/div[2]/div[1]/section[1]/div[2]/table/tbody/tr[{b}]'

        # THIS was timing out so I'm wrapping it in try
        try:
            WebDriverWait(driver, 240).until(
                EC.presence_of_element_located((By.XPATH, table_rowx))
            )
        except Exception:
            print("can't wait for page to load")
            continue

        elem = driver.find_element(by=By.XPATH, value=table_rowx)
        text = elem.text # '1 Play track\nLove this track\nBuddy Holly\n1,380,948 listeners'
        elems = text.split("\n") # ['1 Play track', 'Love this track', 'Buddy Holly', '1,380,948 listeners']
        if len(elems) < 4:
            print(f"skipping {b} because it's not a song")
            print(text)
            print(elems)
            continue
        title = str(elems[2])
        print(title)
        listeners = elems[3].split(" ")[0]

        if row := next(
            (x for x in data if core.sanitize(str(x["song_title"])) == core.sanitize(title)),
            None,
        ):
            row[data_date_range]=listeners
        else:
            print(f"couldn't find {title} in sheet")

    return data

# def update_lastfm(driver, data):
#     """UPDATE THE LASTFM COLUMN IN THE """
#     print("\nupdate_lastfm...")

    
    
#     return scrape_page(driver, d)

    

def main():

    

    # sheet = get_sheet("Weezer Data", "all")

    # data = sheet.get_all_records()
    # # Python >= 3.5 alternative: unpack dictionary keys into a list literal [*newdict]
    # # arbitrarily using the first data row to get the keys
    # headers = [*data[0]]
    

    # countries_of_interest = [x for x in core.countries_of_interest if x in headers]

    driver = core.get_driver()

    sheet = get_sheet("Weezer Data", "all")
    data = sheet.get_all_records()
    

    for page, data_range in zip(pages, ranges):

        open_last_fm_page(driver, page)

        data = scrape_page(driver, data, data_range)
        # update_lastfm(driver)

        # if method in ["all", "albums"]:
        #     update_albums(driver)

        # if method in ["all", "lastfm"]:
        #     update_lastfm(driver)

        # if method in ["all", "time", "timeall", "time28", "time5"]:
        #     update_time_filtered_columns(driver)

        # # update_country_columns(driver, limit)

    update_range(sheet, data)

    driver.close()

    return "Success!"


if __name__ == "__main__":

    main()
