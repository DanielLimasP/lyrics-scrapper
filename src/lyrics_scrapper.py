import bs4
import re
import requests
from pathlib import Path

class Lyrics_Scrapper:
    def __init__(self):
        super().__init__()
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
        content = self.get_soup_content('.main-page')
        self.save_content(content, 'blackened.html')
        #print(self.get_song_info())
        #self.save_content(content, file)
        
    def get_song_info(self):
        content = self.get_soup_content('b')        
        b_stripping = re.compile(r'<b>')
        bb_stripping = re.compile(r'</b>')
        # b_stripping.sub returns a string, so it's ok to use as an arg
        info = bb_stripping.sub('', b_stripping.sub('', str(content)))

        return info

    def get_soup_content(self, attr):
        '''
        get_soup: 
        Gets the content of current page. Needs an attr like 'b' or a classname or id
        '''
        soup_content = self.soup.select(attr)
        return soup_content

    def save_content(self, content, file_name):
        # Save the file
        try:
            new_file = open(file_name, 'w+', encoding='utf-8')
            new_file.write(str(content))
            new_file.close()
            
            return 'File saved'
        except Exception as ex:
            return 'There was a problem: {}'.format(ex)

