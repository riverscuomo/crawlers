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
    1. currently only updates the 'all' sheet in the 'Weezer Data' spreadsheet  
    with latest data from lastfm./weezer

    Currently matches with song_title in the sheet
    """

if "maintenance.py" in sys.argv:
    sys.argv=['lastfmcrawler.py']

# args = my_args.get_args(description)


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

    for i in range(int(fromsongs), int(tosongs) + 1):

        print(f"{i}", end=": ")
        i = str(i)

        table_rowx = f'//*[@id="mantle_skin"]/div[3]/div[2]/div[1]/section[1]/div[2]/table/tbody/tr[{i}]'

        core.wait_for_element(driver, table_rowx)

        elem = driver.find_element(by=By.XPATH, value=table_rowx)
        text = elem.text # '1 Play track\nLove this track\nBuddy Holly\n1,380,948 listeners'
        elems = text.split("\n") # ['1 Play track', 'Love this track', 'Buddy Holly', '1,380,948 listeners']
        if len(elems) < 4:
            print(f"skipping {i} because it's not a song")
            print(text)
            print(elems)
            continue
        title = str(elems[2])
        print(title)
        listeners = elems[3].split(" ")[0].replace(",", "")

        if row := next(
            (x for x in data if core.sanitize(str(x["song_title"])) == core.sanitize(title)),
            None,
        ):
            row[data_date_range]=listeners
        else:
            print(f"couldn't find {title} in sheet")
            # if "All My Favorite Songs (feat. AJR)"==title:
            data.append({"song_title": title, data_date_range: listeners})

    return data


# def consolidate_alt_versions_special(data):
#     """
#     "All My Favorite Songs" and "All My Favorite Songs feat. AJR"
#     """
#     print("consolidate_alt_versions_special...")

#     ajr_index = data.index([x for x in data if "feat. AJR" in str(x["song_title"])][0])
#     ajr = data.pop(ajr_index)
#     all_my_fav = [x for x in data if "All My Favorite Songs" in str(x["song_title"])][0]

#     if "saves_last_28_days" in ajr:
#         all_my_fav["saves_last_28_days"] = str(int(all_my_fav["saves_last_28_days"]) + int(ajr["saves_last_28_days"]))

#     if "streams_last_28_days" in ajr:
#         all_my_fav["streams_last_28_days"] = str(int(all_my_fav["streams_last_28_days"]) + int(ajr["streams_last_28_days"]))

#     if "streams_since_2015" in ajr:
#         all_my_fav["streams_since_2015"] = str(int(all_my_fav["streams_since_2015"]) + int(ajr["streams_since_2015"]))

#     if "lastfm_all" in ajr:
#         all_my_fav["lastfm_all"] = str(int(all_my_fav["lastfm_all"]) + int(ajr["lastfm_all"]))

#     if "lastfm_365_days" in ajr:
#         all_my_fav["lastfm_365_days"] = str(int(all_my_fav["lastfm_365_days"]) + int(ajr["lastfm_365_days"]))

#     if "lastfm_30_days" in ajr:
#         all_my_fav["lastfm_30_days"] = str(int(all_my_fav["lastfm_30_days"]) + int(ajr["lastfm_30_days"]))

#     return data



def main():

    driver = core.get_driver()

    sheet = get_sheet("Weezer Data", "all")
    data = sheet.get_all_records()
    

    for page, data_range in zip(pages, ranges):

        open_last_fm_page(driver, page)

        data = scrape_page(driver, data, data_range)

    data = consolidate_alt_versions_special(data)

    update_range(sheet, data)

    driver.close()

    return "Success!"


if __name__ == "__main__":

    main()
