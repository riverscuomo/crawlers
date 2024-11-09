import logging
import sys
from rich import print

# HAS TO BE ABOVE the other import args or this will not run from maintenance.py cmd line
if "maintenance.py" in sys.argv:
    sys.argv=['spotifyCrawler.py']

import core.__main__ as core
from spotifycrawler.scripts import scripts
from spotifycrawler.scripts import routines
from core.scripts.my_args import args
from _archive.maintenance_config import chromedriver_warning

print("\nspotifycrawler.py")

# sys.path.insert(0, "C:\RC Dropbox\Rivers Cuomo\Apps")
logging.basicConfig(level=logging.INFO)


def main():    

    driver = core.get_driver()

    if type(driver) == str:
        return chromedriver_warning

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
