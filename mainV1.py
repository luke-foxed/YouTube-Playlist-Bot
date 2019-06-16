"""
Author:      Luke Fox
Description: A script to scrape a specificied amount of videos from a given array of channels. These videos can be
             scraped based off a chosen date. From here, the scraped videos are placed into the user's playlist which
             is identified from the playlist ID.
Usage:       [IMPORTANT: This script will need your API KEY and an OAauth client.json file, both of which can be gotten
             from the Google Dev Console]
             Although the script can work by specifying the channel names rather than the channel ID, this takes
             additional usage resources which will limit the ammount of videos that can be sent to the playlist.
             Because of this, it is better to feed in the direct channel IDs, which can be retrived eith from the
             channel URL, or by entering the channel name here -
             http://johnnythetank.github.io/youtube-channel-name-converter/
"""

import json
import sys
import time
import requests

from datetime import datetime, timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from requests.exceptions import HTTPError

youtube = None

API_KEY = 'INSERT_API_KEY'
playlist_id = 'INSERT_PLAYLIST_ID'  # can be gotten from the playlist URL on YouTube

#  channel_names = ['PowerfulJRE']
channel_ids = [
    'UC-lHJZR3Gqxm24_Vd_AJ5Yw', 'UCnQC_G5Xsjhp9fEJKuIcrSw', 'UCzQUP1qoWDoEbmsQxvdjxgQ',
]

current = datetime.utcnow() - timedelta(days=2)  # 0 = today, 1 = yesterday, 7 = last week etc.
date = current.isoformat("T") + "Z"  # youtube 'publishedAt' time format
counter = 0


def main():
    authorize()
    #  Uncomment these two functions and comment out the bottom two if using channel names instead of channel IDs
    """
    channels = get_channel_ids(channel_names)  
    videos = get_videos(channels, 2)
    """
    videos = get_videos(channel_ids, 5)
    add_to_playlist(videos)


def authorize():
    global youtube
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    store = file.Storage('cred.json')
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('INSERT_CLIENT_PATH.json', scopes)
        credentials = tools.run_flow(flow, store)
    try:
        youtube = build('youtube', 'v3', http=credentials.authorize(Http()))
        print('SUCCESSFULLY AUTHORIZED!')
    except HTTPError as error:
        print(error)

    return youtube


def get_channel_ids(channel_names):
    channel_ids = []
    for channel in channel_names:
        request = requests.get(
            'https://www.googleapis.com/youtube/v3/channels?key=%s&forUsername=%s&part=id' % (API_KEY, channel)).json()
        channel_ids.append(request['items'][0]['id'])
    return channel_ids


def get_videos(channel_ids, video_count):
    global date
    video_ids = []
    for i in range(video_count):
        for channel in channel_ids:
            request = requests.get(
                'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=%s&maxResults=%s&order=date&type=video&key=%s&publishedAfter=%s' % (
                    channel, video_count, API_KEY, date)).json()
            print(request)
            if 'dailyUsageLimit' in json.dumps(request):
                print(json.dumps(request, indent=2) + '\n\nExiting...')
                time.sleep(5)
                sys.exit(0)
            else:
                try:
                    video_ids.append(request['items'][i]['id']['videoId'])
                except Exception as error:
                    print(error)
    return video_ids


def add_to_playlist(videos):
    counter = 0
    non_duplicates = check_for_duplicates_locally(videos)
    for video in non_duplicates:
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "position": 0,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video
                    }
                }
            }
        )
        response = request.execute()
        print(response)
        counter += 1
    print('Done! Written %d videos' % counter)


def check_for_duplicates_locally(videos):
    non_duplicates = []
    for video in videos:
        with open('playlist.txt', 'r+') as lines:
            if not lines.read(1):
                print('File is empty, writing video...')
                lines.write('\n' + video)
                non_duplicates.append(video)
            else:
                if video in lines.read():
                    print('Video already in playlist, skipping...')
                    pass
                elif video not in lines.read():
                    print('Writing video...')
                    lines.write('\n' + video)
                    non_duplicates.append(video)
    return non_duplicates


if __name__ == "__main__":
    main()
