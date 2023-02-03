# Crawlers [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)

An experimental project to combine 2 or more poetry packages into a single repo.
These are scrapers and crawlers for various music streaming services. they use python selenium.
I doubt this repo will be of any use to anyone else, but feel free to chime in.
`spotifycrawler` and `lastmcrawler` draw on common code in `core`.
They scrape data from spotify and lastfm respectively, and then use `gspread` to import the data into google sheets.

I use these crawlers to populate https://docs.google.com/spreadsheets/d/10kY2Ti0Gn0jfx92uY0vVntZoJdNTywxKuOfriDoywC0/edit#gid=624343020
From there I make setlists for Weezer shows.

## Installation

Depending on which functions you want to run, you will need the following environment variables:

####  spotifycrawler
You'll need a spotify artists account and the artist_id for that account:
![image](https://user-images.githubusercontent.com/24362267/216662746-ba39b0bb-4cdf-48ab-8318-0c8f3424d8c1.png)

```
SPOTIFY_EMAIL=(for a spotify artist account)
SPOTIFY_PASSWORD=(for a spotify artist account)
```

####  LASTFM
```
LAST_FM_USER = 
LAST_FM_API_KEY = 
LAST_FM_API_SECRET = 
LAST_FM_PASSWORD = 
```

####  GSPREADER For importing and setting data from/to Google Sheets
```
GSPREADER_GOOGLE_CLIENT_EMAIL=client_email_from_your_creds.json
```

### Poetry
poetry init
poetry install


## Running

Once you have completed all the installation steps, cd to one of the crawler directories and run by running `py -m lastfmcrawler`, for example.
Or `poetry run py -m lastfmcrawler` if you are using poetry.


## Contributing
Feel free to make pull requests for any changes you'd like to see.  
