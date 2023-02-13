from rivertils.rivertils import check_positive
import argparse

description = """
    1. updates the 'SPOTIFY' TAB in the SETLIST sheet with latest data from artists.spotify/weezer 28d Streams	28d Listeners	28d Saves	% who save
    2. update the 'ALL TIME STREAMS' '2018' etc columns in the SETLIST sheet
    2. updates the 28-day streams for each [country] column 
    in the countries of interest list here (will skip if the column doesn't exist in the sheet.)

    Currently matches with song_title in the sheet, which is not ideal. Better to match by track_id
    """

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

    # TODO: Add the method names from last.fm script
    parser.add_argument(
    "-m", "--method", help="the method you want to run", required=False, default="all", choices=["all", "albums", "spotify", "time", "timeall", "time28", "time5", "country"]
    )
    parser.add_argument(
    "-t", "--target_sheet", help="the sheet you're updating", required=False, default="all", choices=["all", "weezer_data", "setlist"]
    )
    return parser.parse_args()

args = get_args(description)

method = args.method
target_sheet = args.target_sheet
limit = args.limit