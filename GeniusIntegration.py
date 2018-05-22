# Collect all the data necessary for the neural network
# Use Genius Python API wrapper to get lyric data for artists
# Download and put in directory rapper world mpa data from: https://rapworldmap.com/

import json
import lyricsgenius as genius
import os

bio_data = [] # empty list to be filled with rapper data

api = genius.Genius('Qih5w0Q_T8lDHa4TKLKHyjrsnWfq49zkakiOp_W-dwZ1BoQ_PFdnkMFHSKuskaaw') # initialize Genius API with client token

filename = 'rapworldmap-artists.json' # Can be changed during save as

MAX_NUM_OF_SONGS = 1 # maximum number of songs to be looked at

f = open(filename, 'r', encoding='UTF-8') # open up the file

json_data = json.load(f) # load it into a json format

for rapper in json_data: 
    data = {'name' : rapper['name'], 'coordinates' : rapper['location']['coordinates']} # pull only the important data 
    artist = api.search_artist(rapper['name'], max_songs = MAX_NUM_OF_SONGS, take_first_result = True) # 
    artist.save_lyrics(format = 'json', overwrite = True)
    lyricfile = 'Lyrics_' + rapper['name'].replace(" ", "").replace('"', '') + ".json" 
    if '&' in lyricfile:
    	lyricfile = lyricfile[:lyricfile.index('&')] + '.json'
    try:
        with open(lyricfile, 'r', encoding = 'UTF-8') as f: 
            json_lyrics = json.load(f)
            song_lyrics = ''
            for song in json_lyrics['songs']:
                song_lyrics += '\n' + song['lyrics']
            data.update({'lyrics' : song_lyrics})
            bio_data.append(data)
        # os.unlink(lyricfile)    
    except FileNotFoundError:
    	pass
    
