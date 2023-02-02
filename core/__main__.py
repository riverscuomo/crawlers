
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rivertils.rivertils import check_positive
import os

from dotenv import load_dotenv
load_dotenv()


class Album:
    def __init__(self, title, songs):
        # Init elements #
        self.title = title
        self.count = len(songs)
        self.songs = songs

    def calculate_average_streams(self):
        songs = self.songs
        # To sort the list in place...
        songs.sort(key=lambda x: x.streams, reverse=True)
        songs = songs[3:-1]
        # most_streamed_song = max(songs, key=lambda x: x.streams)
        # songs.pop(songs.index(most_streamed_song))
        # most_streamed_song = max(songs, key=lambda x: x.streams)
        # songs.pop(songs.index(most_streamed_song))
        total_streams = sum(song.streams for song in songs)
        return int(total_streams / self.count)

    def __repr__(self) -> str:
        return f"{self.title} ({self.count})"

class Song:
    def __init__(
        self,
        title=str,
        sequence=int,
        streams=int,
        listeners=int,
        views=int,
        saves=int,
        first_released=str,
    ):
        # Init elements #
        self.title = title
        self.sequence = sequence
        self.streams = streams
        self.listeners = listeners
        self.views = views
        self.saves = saves
        self.first_released = first_released

    def __repr__(self) -> str:
        return f"{self.title} ({self.streams})"

countries_of_interest = [
    "United States",
    # "United Kingdom",
    # "Ireland",
    # # "Germany",
    # # "Czech Republic",
    # "France",
    # "Spain",
    # "Italy",
    "Indonesia",
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

def get_args(description):
    parser = argparse.ArgumentParser(
    description=description
    )

    parser.add_argument(
    "-l",
    "--limit",
    help="the number of songs to search for, descending from the highest value",
    required=False,
    default=50,
    type=check_positive,
    )
    # parser.add_argument(
    #     "-f", "--first", help="the first row you want to get data for", required=False
    # )
    parser.add_argument(
    "-m", "--method", help="the method you want to run", required=False, default="all"
    )
    parser.add_argument(
    "-t", "--target_sheet", help="the sheet you're updating", required=False, default="all", choices=["all", "weezer_data", "setlist"]
    )
    return parser.parse_args()

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
    # THIS was timing out so I'm wrapping it in try
    try:
        WebDriverWait(driver, 240).until(
            EC.presence_of_element_located((By.XPATH, value))
        )
    except Exception:
        print("can't wait for page to load")