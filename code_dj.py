import requests as rq
import re
from bs4 import BeautifulSoup 
from heapq import heappop, heappush



global common_phrases
common_phrases = set()

LYRICS_CONTAINER = 'Lyrics__Container-sc-3d1d18a3-1 bjajog'
SONG_TAGS_CONTAINER = 'SongTags__Container-sc-b55131f0-1 SEhjw'


def setup() -> None:
    global common_phrases

    with open('words_to_avoid.csv', 'r') as file:
        word_list = file.readline().split(',')
        for word in word_list:
            common_phrases.add(word.lower())
    
        

def get_song_lyrics(url: str) -> str:
    if 'genius.com' in url and 'lyrics' in url:    
        response = rq.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        lyric_container = soup.find('div', class_= LYRICS_CONTAINER).get_text(separator=' ')

        lyrics = lyric_container.split('Read More')[1]

        if lyrics:
            with open('lyrics.txt', 'w', encoding='utf-8') as file:
                file.write(lyrics)

                return lyrics

    else:
        print('oopsies! you have inputted an unsupported link. try to upload a link from Genius.')



def record_word_count(url: str) -> list:

    global common_phrases
    word_frequency = {}

    lyrics = get_song_lyrics(url)
    lyrics_list = lyrics.split(' ')

    for word in lyrics_list:
        if word.lower() not in common_phrases:
            word_frequency[word] = 1 + word_frequency.get(word, 0)  

    max_heap = []

    for key in word_frequency.keys():
        heappush(max_heap, (-1 * word_frequency[key], key))
    
    top_five_frequent_words = []

    while len(top_five_frequent_words) < 5:
        top_five_frequent_words.append(heappop(max_heap)[1])

    return top_five_frequent_words


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
                
                similar_songs.append((song_name, song_artist))


        return similar_songs



def compare_songs_by_lyrics(url:str) -> list:

    frequent_lyric_count = record_word_count(url)
    target_genre = get_song_genre(url)
    similar_songs = get_similar_songs(target_genre)



    for song in similar_songs:

        song_name, song_artist = song



        query = f'https://www.genius.com-{song_artist}-{song_name}'






    return None




setup()


print(record_word_count('https://genius.com/Clipse-so-be-it-lyrics'))

# print(get_song_genre('https://genius.com/Clipse-so-be-it-lyrics'))

# get_song_lyrics('https://genius.com/Clipse-so-be-it-lyrics')

compare_songs_by_lyrics('https://genius.com/Clipse-so-be-it-lyrics')




