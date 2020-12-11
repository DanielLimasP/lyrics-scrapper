from lyrics_scrapper import Lyrics_Scrapper
from ap import custom_args

if __name__ == "__main__":
    args = custom_args()
    ls = Lyrics_Scrapper(args)
    ls.get_song_lyrics()
