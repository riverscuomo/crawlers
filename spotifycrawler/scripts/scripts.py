from gspreader.gspreader import get_sheet, update_range
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
import os
# import core
from core import __main__ as core
import core.classes.classes as classes
from core.scripts.my_args import args
import gspreader.gspreader as gspreader


spotify_artist_id = os.getenv("SPOTIFY_ARTIST_ID")
spotify_time_filter_url = f"https://artists.spotify.com/c/artist/{spotify_artist_id}/music/songs?time-filter="

def consolidate_album_data(sheet_data, new_data):
    print("consolidate_album_data...")
    for row in sheet_data:
        for new_row in new_data:
            if str(row["album_title"]).lower() == str(new_row["album_title"]).lower():

                # Update the columns for this album in this new_row
                row.update(new_row)
    existing_albums = [str(row["album_title"]).lower() for row in sheet_data]
    for row in new_data:
        if str(row["album_title"]).lower() not in existing_albums:
            sheet_data.append(row)
    return sheet_data


# def consolidate_alt_versions_special(data):
#     """
#     "All My Favorite Songs" and "All My Favorite Songs feat. AJR"
#     """
#     print("consolidate_alt_versions_special...")

#     ajr_index = data.index([x for x in data if "feat. AJR" in x["song_title"]][0])
#     ajr = data.pop(ajr_index)
#     all_my_fav = [x for x in data if "All My Favorite Songs" in x["song_title"]][0]

#     if "saves_last_28_days" in ajr:
#         all_my_fav["saves_last_28_days"] = str(int(all_my_fav["saves_last_28_days"]) + int(ajr["saves_last_28_days"]))

#     if "streams_last_28_days" in ajr:
#         all_my_fav["streams_last_28_days"] = str(int(all_my_fav["streams_last_28_days"]) + int(ajr["streams_last_28_days"]))

#     if "streams_since_2015" in ajr:
#         all_my_fav["streams_since_2015"] = str(int(all_my_fav["streams_since_2015"]) + int(ajr["streams_since_2015"]))

#     return data


def consolidate_alt_versions(data, new_data, col_header):
    """
    For example "All My Favorite Songs" and "All My Favorite Songs feat. AJR"
    BUT I DON'T HAVE ROWS FOR THE ALT VERSION ANYMORE!!?
    streams_last_28_days
    """
    print("consolidate_alt_versions...")
    # columns_to_consolidate = ["streams", "streams_since_2015"]  # "Youtube"
    # for c in columns_to_consolidate:
    for master_row in data:
        #     if (c in master_row and master_row[c] == "") or master_row[
        #         "song_title_alternate"
        #     ] == "":
        #     continue

        if master_row["track_id_alternate"] == "":
            continue

        print(f"found master version {master_row['song_title']}")
        if slave_rows := [
            x
            for x in new_data
            if str(x["song_title"]).lower() == str(master_row["song_title_alternate"]).lower()
            # and x["song_title"] != master_row["song_title"]
            # and c in x
            and x[col_header] != "" and master_row[col_header] != ""
        ]:
            for slave_row in slave_rows:
                print(
                    f"found slave version {slave_row['song_title']} so consolidating {col_header}"
                )
                master_total = int(str(master_row[col_header]).replace(",", ""))
                slave_total = int(str(slave_row[col_header]).replace(",", ""))
                total = master_total + slave_total
                master_row[col_header] = f"{total:,}"  # add commas
    return data


def consolidate_alt_versions_for_each_country(data, countries_of_interest):
    print("consolidate_alt_versions_for_each_country...")
    for c in countries_of_interest:
        for master_row in data:
            if (c in master_row and master_row[c] == "") or master_row[
                "track_id_alternate"
            ] == "":
                continue
            print(f"found master version {master_row['song_title']}")
            if slave_rows := [
                x
                for x in data
                if x["track_id"] == master_row["track_id_alternate"]
                and x["song_title"] != master_row["song_title"]
                and c in x
                and x[c] != ""
            ]:
                for slave_row in slave_rows:
                    print(
                        f"found slave versions {slave_row['song_title']} and both versions have data for this country"
                    )
                    master_row[c] = int(str(master_row[c]).replace(",", "")) + int(
                        str(slave_row[c]).replace(",", "")
                    )
    return data


def log_into_spotify_site(driver):
    username = os.environ.get("SPOTIFY_EMAIL")
    password = os.environ.get("SPOTIFY_PASSWORD")
    driver.get("https://accounts.spotify.com/en/login")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type = 'text']"))
    )

    email = driver.find_element(by=By.XPATH, value="//input[@type = 'text']")
    email.send_keys(username)
    pw = driver.find_element(by=By.XPATH, value="//input[@type = 'password']")
    pw.send_keys(password)

    login_button_xpath = r'//*[@id="login-button"]/div[1]'

    driver.find_element(by=By.XPATH, value=login_button_xpath).click()

    time.sleep(1)  # rc


def is_valid_album(album):
    """not "deluxe", "remix", "sessions", "christmas"""
    bads = ["deluxe", "remix", "sessions", "christmas", "single"]
    if len(album) < 7:
        return False
    test = album[0].lower()
    # print(test)
    return all(bad not in test for bad in bads)


def scrape_albums(
    driver,
):
    print("scrape_albums...")

    data = []
    search_link = f"https://artists.spotify.com/c/artist/3jOstUTkEu2JkjvRdBA5Gu/music/releases?time-filter==28day"

    driver.get(search_link)

    table = "/html/body/div[2]/div/div/div/div/div/main/div/div/div/div[2]/table"
    # table = '//*[@id="s4a-page-main-content"]/div/div[2]/section[2]/div/table'

    # THIS was timing out so I'm wrapping it in try
    try:
        WebDriverWait(driver, 240).until(
            EC.presence_of_element_located((By.XPATH, table))
        )
    except Exception:
        print("can't wait for page to load")

    elem = driver.find_element(by=By.XPATH, value=table)
    text = elem.text
    return text


def parse_string_into_digit(s):
    s = s.replace(",", "")
    return int(s) if s.isdigit() else 0


def parse_line_to_song(line: str):

    print(line)
    if type(line) == int:
        return

    elems = line.split(" ", maxsplit=1)
    sequence = int(elems[0])
    line = elems[1]
    # print(line)

    elems = line.split(" ")
    elems.reverse()
    date_elems = elems[:3]
    # print(date_elems)
    date_elems.reverse()
    first_release_date = " ".join(date_elems)

    # print(first_release_date)

    title_elems = elems[7:]
    title_elems.reverse()
    # title_elems = title_elems[3:]
    # print(title_elems)
    title = " ".join(title_elems)
    # print(title)

    # print(elems)

    stats_elems = elems[3:7]
    stats_elems.reverse()

    return classes.Song(
        title=title,
        sequence=sequence,
        streams=parse_string_into_digit(stats_elems[0]),
        listeners=parse_string_into_digit(stats_elems[1]),
        views=parse_string_into_digit(stats_elems[2]),
        saves=parse_string_into_digit(stats_elems[3]),
        first_released=first_release_date,
    )


def split_lines_into_albums(lines):
    # print([x for x in enumerate(lines)])

    indexes = [i - 1 for i, x in enumerate(lines) if line_is_start_of_album(x)]
    indexes.append(len(lines))

    albums = []

    for i in range(len(indexes[:-1])):
        start = indexes[i]
        end = indexes[i + 1]
        i += -1
        album = lines[start:end]
        albums.append(album)

    return albums


def line_is_start_of_album(line: str):
    return "Album" in line or "Single" in line or "EP" in line


def parse_country_string(country_string, countries_of_interest):
    # country_row ={}
    countries = country_string.split("\n")
    row = {}
    for country in countries:

        elems = country.split(" ")
        country_name = " ".join(elems[1:-1])
        if country_name not in countries_of_interest:
            continue
        row[country_name] = elems[-1]

    return row


def process_text(text):

    lines = text.split("\n")
    albums = split_lines_into_albums(lines)

    # print(text)
    # print(type(text))
    # print(elems)
    # albums = []
    # album = []
    # for line in lines:
    #     if line == "Album" or line == "EP" or line == "Single" or " EP" in line:

    #         albums.append(album)
    #         album = [lines.index(line) - 1]
    #     else:
    #         album.append(line)

    # # to catch the very last album (the blue album)
    # albums.append(album)

    # for album in albums:
    #     # title_of_next_album = album.pop(-1)
    #     index = albums.index(album) + 1
    #     print(index)

    #     albums[index].insert(0, title_of_next_album)
    #     try:
    #         album.pop(2)
    #         album.pop(1)
    #     except:
    #         pass

    albums = [x for x in albums if is_valid_album(x)]
    # print(albums)
    # print(len(albums))

    objs = []
    for album in albums:
        title = album[0]
        album = album[3:]
        album.insert(0, title)
        songs = [parse_line_to_song(x) for x in album[1:]]
        album = classes.Album(title=title, songs=songs)
        # print(album, album.calculate_average_streams())
        objs.append(album)

    return objs


def scrape_page(driver, data, date_range: str,fromsongs=1, tosongs=200):
    print("scrape_page")
    # data = [] # if you want to wipe out the sheet and start over

    print(f"from {fromsongs} to {tosongs}")

    driver.get(spotify_time_filter_url+date_range)

    for b in range(int(fromsongs), int(tosongs) + 1):

        print(f"b: {b}")
        b = str(b)
        table_rowx = f'//*[@id="s4a-page-main-content"]/div/div[2]/section[2]/div/table/tbody/tr[{b}]'

        # THIS was timing out so I'm wrapping it in try
        core.wait_for_element(driver, table_rowx, timeout=100)

        elem = driver.find_element(by=By.XPATH, value=table_rowx)
        text = elem.text
        elems = text.split("\n")
        # rank = elems[0]
        title = elems[1]
        subelems = elems[2].split(" ")

        streams28 = subelems[0]
        listeners28 = subelems[1]
        saves28 = subelems[4]

        row = {
            "Song Title": title,
            "28d Streams": streams28,
            "28d Listeners": listeners28,
            "28d Saves": saves28,
            "% who save": (
                float(saves28.replace(",", "")) / float(listeners28.replace(",", ""))
            ),
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        }

        # for x in allData:
        #     if x['Song Title'] == row['Song Title']:
        #         x = row
        #         break
        # if there wasn't a match go ahead and append this row
        data.append(row)

        elem.click

        continue

    return data


def scrape_country_data(driver, countries_of_interest, fromsongs=1, tosongs=75, ):
    """Get the streams for each song in the coutries of interest. (Default is US)"""

    # data = [] # if you want to wipe out the sheet and start over

    print("scrape_country_data...")
    print(f"from song {fromsongs} to {tosongs}")
    search_link = "https://artists.spotify.com/c/artist/3jOstUTkEu2JkjvRdBA5Gu/music/songs"
    

    country_data = []

    for b in range(int(fromsongs), int(tosongs) + 1):

        # YOU NEED TO RELOAD THE PAGE EVERY TIME to CLICK ON A NEW SONG
        driver.get(search_link)

        print(f" - {b}: ", end="")
        b = str(b)
        # table_row_for_this_songx = f'//*[@id="s4a-page-main-content"]/div/div[2]/section[2]/div/table/tbody/tr[{b}]'
        # table_row_for_this_songx = f'//*[@id="s4a-page-main-content"]/div/div[2]/section[2]/div/table/tbody/tr[{b}]/td[2]/div'
        table_row_for_this_songx = f'//*[@id="s4a-page-main-content"]/div/div[2]/section[2]/div/table/tbody/tr[{b}]/td[2]/div/div/span'

        core.wait_for_element(driver, table_row_for_this_songx)
        elem = driver.find_element(by=By.XPATH, value=table_row_for_this_songx)
        song_title = elem.text
        # song_title = text.split("\n")[1]
        elem.click()

        # location_buttonx = '//*[@id="s4a-page-main-content"]/div/div[2]/div[1]/div[2]/div/div[2]/ul/li[3]/a'
        location_buttonx = '//*[@id="s4a-page-main-content"]/div/div[2]/div[1]/div[2]/ul/li[3]/a'
        # location_buttonx = '//*[@id="s4a-page-main-content"]/div/div[2]/div[1]/div[2]/ul/li[3]/a'
        core.wait_for_element(driver,location_buttonx )
        elem = driver.find_element(by=By.XPATH, value=location_buttonx)
        elem.click()

        country_tablex = '//*[@id="where-they-listen"]/div[2]/div/div/table/tbody'
        core.wait_for_element(driver, country_tablex )
        elem = driver.find_element(by=By.XPATH, value=country_tablex)

        row = parse_country_string(elem.text, countries_of_interest)
        row["song_title"] = song_title
        print(row)

        country_data.append(row)

            # continue
    return country_data


def scrape_time_filter(
    driver,
    time_filter: str,
    fromsongs=1,
):
    print("scraping time filter:", time_filter)
    data = []

    print(f"from {fromsongs} to {args.limit}")
    search_link = f"{spotify_time_filter_url}{time_filter}"

    driver.get(search_link)

    for i in range(int(fromsongs), int(args.limit) + 1):

        
        i = str(i)
        # table_rowx = "/html/body/div[2]/div/div/div/div/div/main/div/div/div/div[2]/table"
        table_rowx = f"/html/body/div[2]/div/div/div/div/div/main/div/div/div/div[2]/section[2]/div/table/tbody/tr[{i}]"

        # THIS was timing out so I'm wrapping it in try
        core.wait_for_element(driver, table_rowx, timeout=40)

        elem = driver.find_element(by=By.XPATH, value=table_rowx)
        text = elem.text
        elems = text.split("\n")
        # rank = elems[0]
        title = elems[1]
        subelems = elems[2].split(" ")
        streams = subelems[0]

        row = {"song_title": title}
        
        if time_filter == 'last28days':
            column = "streams_last_28_days"
            row["saves_last_28_days"] = subelems[4].replace(",", "")
        elif time_filter == "all":
            column = "streams"
        elif time_filter == "last5years":
            column = "streams_since_2015"
        row[column] = streams.replace(",", "")
        

        print(f"{i}: {row}")
        # print(")

        # for x in allData:
        #     if x['Song Title'] == row['Song Title']:
        #         x = row
        #         break
        # if there wasn't a match go ahead and appen this row
        data.append(row)

        elem.click

        continue

    # data = consolidate_alt_versions(data)
    return data


def custom_update(sheet_data: list, new_data: list, matching_field: str):
    """ update the sheet_data with the new_data (if there's a matching row in the new data)"""
    print(f"custom_update on {matching_field}")
    for row in sheet_data:
        for new_row in new_data:
            if gspreader.sanitize_key(str(row[matching_field])) == gspreader.sanitize_key(str(new_row[matching_field])):

                keys = list(new_row.keys())
                keys = [x for x in keys if x != matching_field]
                for key in keys:
                    row[f"spotify_{key}"] = new_row[key]

    return sheet_data


def fetch_new_datas(driver):
    datas = []

    # # get all the new spotify data
    # if args.method in ["all", "time", "timeall"]:
    #     all_time_data = scrape_time_filter(driver, "all")
    #     datas.append(all_time_data)        
    if args.method in ["all", "time", "time5"]:
        since_2015_data = scrape_time_filter(driver, "last5years")
        core.consolidate_alt_versions_special(since_2015_data)
        datas.append(since_2015_data)        
    if args.method in ["all", "time", "time28"]:
        last_28_days_data = scrape_time_filter(driver, "last28days", fromsongs=1)
        core.consolidate_alt_versions_special(last_28_days_data)
        datas.append(last_28_days_data)
    return datas
            

        # data = gspreader.update_sheet_data_by_matching_key(data, all_time_data, "song_title")
        # data = consolidate_alt_versions(data, all_time_data, "streams")
        # data = gspreader.update_sheet_data_by_matching_key(data, since_2015_data,"song_title")
        # data = consolidate_alt_versions(data, since_2015_data, "streams_since_2015")
        # data = gspreader.update_sheet_data_by_matching_key(data, last_28_days_data, "song_title")
        # data = consolidate_alt_versions(data, last_28_days_data, "streams_last_28_days")
    # for sheet in sheets:
    #     print(f"updating {sheet.title}...")

        # # get the old sheet data again
        # sheet_data = sheet.get_all_records()
        # data = update_sheet_data(sheet_data, data)
       