from pathlib import Path # Path for getting cwd
import bs4 # BeautifulSoup for html processing
import re # For regexp processing within html docs
import requests # For Making the initial request
import argparse # For creating a simple argparser
import os # Getting dirs and stuff

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

        info_len = len(self.get_song_info())

        # Artist, then song, then album
        if info_len == 3:
            artist, song, album = self.get_song_info()
        else:
            info = self.get_song_info()
            artist = info[0]
            song = info[1]
            album = info[2]


        print('Dowloading lyrics...')
        print(CYAN + '''
        artist: {}
        album: {}
        song: {}
        '''.format(artist, album, song)+ LIGHT_GRAY)

        # Need to get rid of the " " and replace spaces with _
        song = song[1:-1]
        song = song.replace(' ', '_')
        # Same for the album
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
        # Content is a list of ocurrences of said class
        albums_title = self.get_soup_content('.songinalbum_title')
        info = self.get_soup_content('b')

        artist = str(info[0])
        song_title = str(info[1])
        albums_title = str(info[2])

        return (artist, song_title, albums_title)


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

