import logging
import sys
from rich import print
import os

import core.__main__ as core
from spotifycrawler.scripts import scripts
from spotifycrawler.scripts import routines
from core.scripts.my_args import args

print("\nspotifycrawler.py")



if "maintenance.py" in sys.argv:
    sys.argv=['spotifyCrawler.py']

# sys.path.insert(0, "C:\RC Dropbox\Rivers Cuomo\Apps")
logging.basicConfig(level=logging.INFO)


def main():    

    driver = core.get_driver()

    scripts.log_into_spotify_site(driver)

    if args.method in ["all", "albums"]:
        routines.update_albums(driver)

    if args.method in ["all", "spotify"]:
        routines.update_spotify_tab(driver)

    if args.method in ["all", "time", "timeall", "time28", "time5"]:
        routines.update_time_filtered_columns(driver)

    if args.method in ["all", "country"]:
        routines.update_country_columns(driver)

    driver.close()

    return "Success!"


if __name__ == "__main__":

    main()
