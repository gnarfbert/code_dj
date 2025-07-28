import requests as rq
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
            common_phrases.add(word)
    
        

def get_song_lyrics(url: str) -> str:
    if 'genius.com' in url and 'lyrics' in url:    
        response = rq.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        lyrics = ''

        html_containers = soup.find('div', class_= LYRICS_CONTAINER).contents

        for span in html_containers:
            lyrics += span.text


        lyrics = lyrics.split('Read More')[1]

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



def get_similar_songs(genre:str) -> list:
    similar_songs = []
    with open('spotify_songs.csv', 'r', encoding= 'utf-8') as file:
        file.readline()

        while True:
            line = file.readline()
            if line == '':
                break
            
            song_information = line.split(',')

            if song_information[9].lower() == genre.lower():
                similar_songs.append((song_information[1], song_information[2]))


        return similar_songs



def compare_songs_by_lyrics(url:str) -> list:

    frequent_lyric_count = record_word_count(url)
    target_genre = get_song_genre(url)
    similar_songs = get_similar_songs(target_genre)

    
    return None




setup()

print(record_word_count('https://genius.com/Clipse-so-be-it-lyrics'))

# print(get_song_genre('https://genius.com/Clipse-so-be-it-lyrics'))




