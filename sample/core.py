import requests
from bs4 import BeautifulSoup
import re
import json

class Youtube:
    """
    Class to scrape Youtube channel
    """
    def __init__(self, url: str):
        self.url = url
        if not re.match(r'.*\w*\/c\/.*\/videos',self.url):
            raise Exception(f"Wrong url {self.url} specified. It needs to have the following format: 'https://www.youtube.com/c/accountname/videos'")
        self.headers = {"Accept-Language": "en-US,en;q=0.5"}
        self.yt_content = []
    
    # Returning a list of the last 30 video titles
    def titles(self):
        if self.yt_content == []:
            self.scrape()
        return [video.get('title') for video in self.yt_content]

    # Returning a list of the last 30 video ids
    def id(self):
        if self.yt_content == []:
            self.scrape()
        return [video.get('id') for video in self.yt_content]

    # Returning a list of the last 30 video long titles, consistent of title, date, viewcount.
    def long_title(self):
        if self.yt_content == []:
            self.scrape()
        return [video.get('long_title') for video in self.yt_content]

    # Returning a list of the last 30 video published-at dates
    def published_at(self):
        if self.yt_content == []:
            self.scrape()
        return [video.get('published') for video in self.yt_content]

    # Returning a list of the last 30 video viewcounts
    def viewcount(self):
        if self.yt_content == []:
            self.scrape()
        return [video.get('viewcount') for video in self.yt_content]
    
    # Returning a list of the last 30 video urls
    def url(self):
        if self.yt_content == []:
            self.scrape()
        return [video.get('url') for video in self.yt_content]
    
    # Returning a list of the last 30 video durations
    def duration(self):
        if self.yt_content == []:
            self.scrape()
        return [video.get('duration') for video in self.yt_content]

    # Returning a list of the last 30 videos as a dictionary
    def complete_overview():
        if self.yt_content == []:
            self.scrape()
        return self.yt_content

    # Function that scrapes the data
    def scrape(self):
        yt_content = []
        output = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(output.text, 'html.parser')
        output = [str(element) for element in soup.find_all('script') if 'window["ytInitialData"]' in str(element)][0]
        json_output = json.loads(re.search(r'ytInitialData"]\s{1}.{1}\s{1}(.*);', output).group(1))
        videos = json_output.get('contents').\
        get('twoColumnBrowseResultsRenderer').\
        get('tabs')[1].\
        get('tabRenderer').\
        get('content').\
        get('sectionListRenderer').\
        get('contents')[0].\
        get('itemSectionRenderer').\
        get('contents')[0].\
        get('gridRenderer').\
        get('items')
        for video in videos:
            yt_content.append({
                'id':video.get('gridVideoRenderer').\
                    get('videoId'),
                'title': video.get('gridVideoRenderer').\
                    get('title').\
                    get('runs')[0].\
                    get('text'),
                'long_title': video.get('gridVideoRenderer').\
                    get('title').\
                    get('accessibility').\
                    get('accessibilityData').\
                    get('label'),
                'published': video.get('gridVideoRenderer').\
                    get('publishedTimeText').\
                    get('simpleText'),
                'viewcount': video.get('gridVideoRenderer').\
                    get('viewCountText').\
                    get('simpleText'),
                'url': video.get('gridVideoRenderer').\
                    get('navigationEndpoint').\
                    get('commandMetadata').\
                    get('webCommandMetadata').\
                    get('url'),
                'duration': video.get('gridVideoRenderer').\
                    get('thumbnailOverlays')[0].\
                    get('thumbnailOverlayTimeStatusRenderer').\
                    get('text').\
                    get('accessibility').\
                    get('accessibilityData').\
                    get('label')
                })
        self.yt_content = yt_content


