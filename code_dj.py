import requests as rq
import spacy
import re 
from bs4 import BeautifulSoup 


nlp = spacy.load('en_core_web_md')



LYRICS_CONTAINER = 'Lyrics__Container-sc-3d1d18a3-1 bjajog'
LYRICS_HEADER = 'LyricsHeader__Container-sc-5af38d6b-1 ksyvqp'
SONG_TAGS_CONTAINER = 'SongTags__Container-sc-b55131f0-1 SEhjw'


    
    
def get_song_lyrics(url: str) -> str:
    try:   
        response = rq.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        lyric_container = soup.find('div', class_= LYRICS_CONTAINER).find('div', class_= LYRICS_HEADER).decompose()
        lyric_container = soup.find('div', class_= LYRICS_CONTAINER).get_text(separator= ' ')

        lyrics = re.split(r'\xa0', lyric_container)[0]
        print(len(lyrics))

        if lyrics:
            return lyrics

    except AttributeError:
        pass



def compare_lyrics_similarity(song1: str, song2:str) -> int:
    lyrics1 = nlp(song1)
    lyrics2 = nlp(song2)
    filtered_lyrics1 = nlp(' '.join([str(word) for word in lyrics1 if word.pos_ in ['NOUN', 'PROPN']]))
    filtered_lyrics2 = nlp(' '.join([str(word) for word in lyrics2 if word.pos_ in ['NOUN', 'PROPN']]))

    print(filtered_lyrics1)
    print(filtered_lyrics2)
    print(filtered_lyrics1.similarity(filtered_lyrics2))
    return filtered_lyrics1.similarity(filtered_lyrics2)


def get_song_genre(url:str) -> str:

    if 'genius' in url and 'lyrics' in url:
        response = rq.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        genre = soup.find('div', class_= SONG_TAGS_CONTAINER).contents[0].text
        
        return genre
    
    else:
        print('oopsies! you have inputted an unsupported link. try to upload a link from Genius.')



def get_similar_songs(target_genre:str) -> list:
    similar_songs = []
    with open('spotify_songs.csv', 'r', encoding= 'utf-8') as file:
        file.readline()

        while True:
            line = file.readline()
            if line == '':
                break
            
            song_information = line.split(',')
            
            song_genre = song_information[9]

            if song_genre.lower() == target_genre.lower():
                
                song_name = song_information[1]
                song_artist = song_information[2]

                song_artist = song_artist.replace(' ', '-')
                song_name = re.sub('\s*\(feat\..*?\)\s*', '',song_name).replace(' ', '-')
                genius_url = f'https://www.genius.com/{song_artist}-{song_name}-lyrics'

                
                similar_songs.append(genius_url)

        return similar_songs



def compare_songs_by_lyrics(url:str) -> list:

    recommended_songs = []

    user_song_lyrics = get_song_lyrics(url)
    target_genre = get_song_genre(url)
    similar_songs = get_similar_songs(target_genre)









    print(recommended_songs)





# print(record_word_count('https://genius.com/Clipse-so-be-it-lyrics'))

# print(get_song_genre('https://genius.com/Clipse-so-be-it-lyrics'))

# get_song_lyrics('https://genius.com/Clipse-so-be-it-lyrics')

# compare_songs_by_lyrics('https://genius.com/Clipse-so-be-it-lyrics')

# get_similar_songs('rap','drake')

print(get_similar_songs('rap'))





