# Collect all the data necessary for the neural network
# Use Genius Python API wrapper to get lyric data for artists
# Download and put in directory rapper world mpa data from: https://rapworldmap.com/

import json
import lyricsgenius as genius
import os

bio_data = [] # empty list to be filled with rapper data

api = genius.Genius('Qih5w0Q_T8lDHa4TKLKHyjrsnWfq49zkakiOp_W-dwZ1BoQ_PFdnkMFHSKuskaaw') # initialize Genius API with client token

filename = 'rapworldmap-artists.json' # Can be changed during save as

MAX_NUM_OF_SONGS = 30 # maximum number of songs to be looked at

with open(filename, 'r', encoding='UTF-8') as f: # open up the file

    	json_data = json.load(f) # load it into a json format

for rapper in json_data: 
    data = {'name' : rapper['name'], 'coordinates' : rapper['location']['coordinates']} # pull only the important data 
    if float(rapper['location']['coordinates'].split(',')[0]) > -30: #limit to the Americas
    	pass
    else:
        try: 
            artist = api.search_artist(rapper['name'], max_songs = MAX_NUM_OF_SONGS, take_first_result = True) # search for artist on Genius
            lyricfile = 'Lyrics_' + rapper['name'].replace(" ", "").replace('"', '').replace(".", "") #Get rid of all characters that hurt files
            artist.save_lyrics(format = 'json', overwrite = True, filename = lyricfile) # save the lyrics
            lyricfilewjson = lyricfile + ".json" # add a .json extension to the file name (done automatically above by lyricsgenius lib) 
            with open(lyricfilewjson, 'r', encoding = 'UTF-8') as f: 
                json_lyrics = json.load(f) # load file into json
                song_lyrics = '' # empty string for song lyrics
                for song in json_lyrics['songs']:
                    song_lyrics += '\n' + song['lyrics'] # add all the songs lyrics to a string
                data.update({'lyrics' : song_lyrics}) # put it in a dictionary
                bio_data.append(data) # create a list of dictionaries 
            os.unlink(lyricfilewjson) # remove the json file created to lessen headaches
        except AssertionError:
    	    pass
with open('outputfile', 'w') as fout:
    json.dump(bio_data, fout) # write the data to some final location


