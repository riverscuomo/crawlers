# from gspreader.gspreader import get_sheet, gspreader.update_range
from spotifycrawler.scripts import scripts
from core import __main__ as core
from core.scripts.my_args import args
import gspreader.gspreader as gspreader

def update_albums(driver):
    """UPDATE THE ALBUM STREAMS COLUMN IN THE setlist SHEET"""
    print("\nupdate_albums...")

    text = scripts.scrape_albums(driver)
    albums = scripts.process_text(text)
    new_data = [
        {"album_title": x.title, "28-day streams": x.calculate_average_streams()}
        for x in albums
    ]

    sheet = gspreader.get_sheet("Setlist", "albums")
    sheet_data = sheet.get_all_records()

    data = scripts.consolidate_album_data(sheet_data, new_data)

    gspreader.update_range(sheet, data)


def update_country_columns(driver):
    """UPDATE THE COUNTRY COLUMNS IN THE SETLIST SHEET"""
    print("\nupdate_country_columns...")
    sheet = gspreader.get_sheet("Setlist", 0)

    data = sheet.get_all_records()
    # Python >= 3.5 alternative: unpack dictionary keys into a list literal [*newdict]
    # arbitrarily using the first data row to get the keys
    headers = [*data[0]]

    countries_of_interest = [x for x in core.countries_of_interest if x in headers]

    country_data = scripts.scrape_country_data(driver, countries_of_interest, tosongs=args.limit)

    data = gspreader.update_sheet_data_by_matching_key(data, country_data, "song_title")
    data = scripts.consolidate_alt_versions_for_each_country(data, countries_of_interest)
    gspreader.update_range(sheet, data)


def update_spotify_tab(driver):
    """UPDATE THE SPOTIFY TAB IN THE setlist WORKBOOK"""
    print("\nupdate_spotify_tab...")
    sheet = gspreader.get_sheet("Setlist", "spotify")
    data = sheet.get_all_records()
    data = scripts.scrape_page(driver, data, "28day")

    gspreader.update_range(sheet, data)


def update_time_filtered_columns(driver):
    """UPDATE THE ALL TIME STREAMS, last 5 years, and last 28 days COLUMNs IN THE setlist and Weezer Data sheets"""
    print("\nupdate_time_filtered_columns on ", end="")

    new_datas = scripts.fetch_new_datas(driver)

    # get all the old sheet data
    sheets = []
    if args.target_sheet in ["all", "weezer_data"]:
        sheets.append(gspreader.get_sheet("Weezer Data", "all"))
    if args.target_sheet in ["all", "setlist"]:
        sheets.append(gspreader.get_sheet("Setlist", 0))    

    for sheet in sheets:
        print(sheet.title)

        # get the old sheet data and update it
        data = sheet.get_all_records()

        # consolidate the new data with the old data
        for new_data in new_datas:
            # data = gspreader.update_sheet_data_by_matching_key(data, new_data, "song_title")
            data = scripts.custom_update(data, new_data, "song_title")        

        gspreader.update_range(sheet, data)



def update_weezer_data(driver):
    """UPDATE THE all TAB IN THE WEEZER DATA WORKBOOK"""
    print("\nupdate_weezer_data...")
    sheet = gspreader.get_sheet("Weezer Data", "all")
    data = sheet.get_all_records()
    data = scripts.scrape_page(driver, data, "28day")
    data = scripts.scrape_page(driver, data, "last5years")

    gspreader.update_range(sheet, data)

