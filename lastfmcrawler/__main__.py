import sys

import logging
import gspreader.gspreader as gspreader
from selenium.webdriver.common.by import By
from rich import print
from rivertils import *
import core.__main__ as core
from _archive.maintenance_config import chromedriver_warning
from dotenv import load_dotenv
load_dotenv()

print("\nlastfmcrawler.py")
if "maintenance.py" in sys.argv:
    sys.argv=['lastfmcrawler.py']
# sheet = get_sheet("")
description = """
    1.  updates the 'all' sheet in the 'Weezer Data' spreadsheet and the data sheet in Setlist spreadsheet
    with latest data from lastfm./weezer

    Currently matches with song_title in the sheet

    """
print(sys.argv)


logging.basicConfig(level=logging.INFO)

class LastFmRequest:
    def __init__(self, url, date_preset, sheet_header):
        self.url = url
        self.date_preset = date_preset
        self.sheet_header = sheet_header
    
    def __repr__(self):
        return f"{self.url} {self.date_preset} {self.sheet_header}"


def build_requests():
    base_url = "https://www.last.fm/music/Weezer/+tracks?"
    date_presets = [
       {"date_preset": "ALL", "sheet_header":"lastfm_all"},        
        {"date_preset":"LAST_30_DAYS", "sheet_header":"lastfm_30_days"},       
        {"date_preset":"LAST_365_DAYS", "sheet_header":"lastfm_365_days"}
         # "LAST_7_DAYS",
        # "LAST_90_DAYS",
        # "LAST_180_DAYS",
    ]

    requests = []
    for date_preset in date_presets:
        for i in range(1, 11):
            date= date_preset["date_preset"]
            requests.append(LastFmRequest(url=f"{base_url}date_preset={date}&page={i}", date_preset=date, sheet_header=date_preset["sheet_header"]))
        # requests.extend(
        #     f"{base_url}date_preset={date_preset}&page={i}"
            
        # )
    return requests


def open_last_fm_page(driver, page):
    print(f"\nopen_last_fm_page: {page}")
    driver.get(page)
    print("opened last.fm")


def scrape_page(driver, request: LastFmRequest, data, fromsongs=1, tosongs=53):
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
        data.append({"song_title": title, request.sheet_header: listeners})

        # if row := next(
        #     (x for x in data if gspreader.sanitize_key(str(x["song_title"])) == gspreader.sanitize_key(title)),
        #     None,
        # ):
        #     row[data_date_range]=listeners
        # else:
        #     print(f"couldn't find {title} in sheet")
        #     # if "All My Favorite Songs (feat. AJR)"==title:
        #     data.append({"song_title": title, data_date_range: listeners})

    return data




def main():

    driver = core.get_driver()

    if type(driver) == str:
        return chromedriver_warning

    new_data = []

    requests = build_requests()

    for request in requests:

        open_last_fm_page(driver, request.url)

        new_data = scrape_page(driver, request, new_data)

    new_data = core.consolidate_alt_versions_special(new_data)
    
    driver.close()    
    
    """ Update the 2 sheets with the new data """
    sheets = [
        ("Weezer Data", "all"), 
        ("Setlist", "data")
    ]

    for sheet_tuple in sheets:
    
        sheet = gspreader.get_sheet(sheet_tuple[0], sheet_tuple[1])
        sheet_data = sheet.get_all_records()
        data = gspreader.update_sheet_data_by_matching_key(sheet_data, new_data, "song_title")
        gspreader.update_range(sheet, data)

    return "Success!"




if __name__ == "__main__":

    main()
