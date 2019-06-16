# YouTube Playlist Bot

## Description

This script will automatically scrape a specified number of videos from selected YouTube channels that have been published within a given date. These scraped videos will have their IDs stored locally and then are added to a specified playlist. The local IDs will be checked before writing to the playlist to ensure no duplicates are being added to the playlist.

## Installation
First, install the requirements by running the command `pip install -r requirements.txt`.

Then, a client ID and API key will be needed, which can be created in the Google Dev Console.

### Creating an API Key: 
1.  Go to https://console.developers.google.com
2. Create a new project and add the YouTube Data API
3. On the 'Credentials' section of your project, select 'Create Credentials' and select 'API Key'. This will generate an API key to use with the script

### Creating an Oauth Client ID: 

1. Steps 1-3 as listed above, with the exception that on step 3 select 'OAuth Client ID
2. Choose 'other' as the application type
3. Back on the credentials screen, there will be a download icon to the right of your OAuth Client ID. This is the json file that will be used in the script

## Usage

Once the necessary credentials have been fed in, run the script once to authorize the user and store the necessary tokens for permanent authorization. Then, simply add your channel IDs and the playlist ID and run the script. 

**IMPORTANT:** The channels can also be retrieved through the channel name rather than the channel ID, but this spends on the daily usage limit imposed by Google since it uses requests to lookup the channel name and change it to an ID. Because of this, it is better to simply feed in the channel ID. For channels with custom URLs (no ID in the URL), use this link - http://johnnythetank.github.io/youtube-channel-name-converter/

## Notes

- Assuming the lookups are done using channel IDs rather than channel names, this script should allow for a total of **27 videos** to be written to a playlist before the usage limit is reached. 

- Duplicate video lookups can be done through the API but this, again, will impact the usage limit. Because of this, duplicates validation is done locally simply by reading the video IDs from a text file.

- Your quota for your daily usage limit can be checked by clicking on your project in the Google Dev Console Dashboard, then clicking 'Quotas'.
