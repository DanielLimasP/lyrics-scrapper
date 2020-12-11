import bs4
import re
import requests
from pathlib import Path
import os

# ANSI COLORS:
RED = "\033[0;31m"
GREEN = "\033[0;32m"
CYAN = "\033[0;36m"
LIGHT_GRAY = "\033[0;37m"

class Lyrics_Scrapper:
    def __init__(self, args):
        super().__init__()
        # It's kinda redundant to have both the url and the res together
        self.args = args
        self.url = args['url']
        self.res = requests.get(self.url)
        self.soup = bs4.BeautifulSoup(self.res.text, 'html.parser')

        # Request validation
        try:
            self.res.raise_for_status()
        except Exception as ex:
            print(RED + 'There was a problem: {}'.format(ex)+ LIGHT_GRAY)

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

        print('Dowloading lyrics...')
        print(CYAN + '''
        artist: {}
        album: {}
        song: {}
        '''.format(artist, album, song)+ LIGHT_GRAY)

        # Need to get rid of the " " and replace spaces with _
        song = song[1:-1]
        song = song.replace(' ', '_')
        # Same for album
        album = album[1:-1]
        album = album.replace(' ', '_')
        artist = artist.replace(' ', '_')

        song = song + '.html'

        print(self.save_content(content, song, artist, album))

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

    # TODO: Fix the problem with special chars when saving
    def save_content(self, content, song, artist, album):
        '''
        :type attr: str, str, str
        :rtype: str
        
        save_content: 
        Saves the requested song lyrics
        '''
        cwd = Path.cwd()
        # Save the file
        try:
            path_exists = os.path.exists('Lyrics'+ '/' +artist+ '/' +album)
            if path_exists: 
                new_file = open('Lyrics'+ '/' +artist+ '/' +album+ '/' +song, 'w+', encoding='utf-8')
                new_file.write(str(content))
                new_file.close()
                return GREEN +'File saved'+ LIGHT_GRAY
            else:
                # Create the new dir for the album
                path_exists = os.path.exists('Lyrics' + '/' +artist)
                if path_exists:
                    Path('Lyrics'+ '/' +artist+ '/' + album).mkdir()
                else:
                    Path('Lyrics'+ '/' +artist).mkdir()
                    Path('Lyrics'+ '/' +artist+ '/' + album).mkdir()
                new_file = open('Lyrics'+ '/' +artist+ '/' +album+ '/' +song, 'w+', encoding='utf-8')
                new_file.write(str(content))
                new_file.close()
                return 'File saved'
        except Exception as ex:
            return RED +'There was a problem: {}'.format(ex)+ LIGHT_GRAY
            

    def set_url(self, url):
        '''
        :type attr: str
        :rtype: None
        
        set_url: 
        setter for the url and req
        '''
        self.url = url
        self.res = requests.get(self.url)

