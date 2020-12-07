import bs4
import re
import requests
from pathlib import Path
import os

class Lyrics_Scrapper:
    def __init__(self):
        super().__init__()
        # It's kinda redundant to have both the url and the res together
        self.url = 'https://www.azlyrics.com/lyrics/metallica/theshorteststraw.html'
        self.res = requests.get(self.url)
        self.soup = bs4.BeautifulSoup(self.res.text, 'html.parser')

        # Request validation
        try:
            self.res.raise_for_status()
        except Exception as ex:
            print('There was a problem: {}'.format(ex))

    # It really gets the main content of the page
    def get_song_lyrics(self):
        '''
        :type attr: None
        :rtype: None
        
        get_song_lyrics: 
        (Almost) Gets the req song lyrics and saves it to a file
        '''
        content = self.get_soup_content('.main-page')
        artist, song, album = self.get_song_info()
        # Need to get rid of the " " and replace spaces with _
        song = song[1:-1]
        song = song.replace(' ', '_')
        # Same for album
        album = album[1:-1]
        album = album.replace(' ', '_')
        artist = artist.replace(' ', '_')

        song = song + '.html'

        self.save_content(content, song, artist, album)
        
    def get_song_info(self):
        '''
        :type attr: None
        :rtype: List[]
        
        get_song_info: 
        Gets the Artist, the song name and the album from curr page
        '''
        content = self.get_soup_content('b')
        info_list = []

        for element in content:
            b_strip = re.compile(r'<b>')
            bb_strip = re.compile(r'</b>')
            # b_strip.sub returns a string, so it's ok to use it as an arg
            info_list.append(bb_strip.sub('', b_strip.sub('', str(element))))

        return info_list

    def get_soup_content(self, attr):
        '''
        :type attr: str
        :rtype: soup_content
        
        get_soup: 
        Gets the content of current page. Needs an attr like 'b' or a classname or id
        '''
        soup_content = self.soup.select(attr)
        return soup_content

    def save_content(self, content, song, artist, album):
        cwd = Path.cwd()
        # Save the file
        try:
            if os.path.exists(cwd / artist / album):
                new_file = open(artist / album / song, 'w+', encoding='utf-8')
                new_file.write(str(content))
                new_file.close()
                print('File saved')
                return 'File saved'
            else: 
                # Create the new dir for the album
                Path.mkdir(cwd / artist / album)
                new_file = open(artist / album / song, 'w+', encoding='utf-8')
                new_file.write(str(content))
                new_file.close()
                print('File saved')
                return 'File saved'
        except Exception as ex:
            print('There was a problem: {}'.format(ex))
            return 'There was a problem: {}'.format(ex)

    def set_url(self, url):
        self.url = url
        self.res = requests.get(self.url)

