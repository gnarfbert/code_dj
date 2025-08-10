import requests as rq
import spacy
import re 
import concurrent.futures
import random
from bs4 import BeautifulSoup 


nlp = spacy.load('en_core_web_md')


# DO NOT EDIT: These constant values help the scraping function identify the target HTML elements
LYRICS_CONTAINER = 'Lyrics__Container-sc-39b434ea-1 gHGicG'
LYRICS_HEADER = 'LyricsHeader__Container-sc-5af38d6b-1 ksyvqp'
SONG_TAGS_CONTAINER = 'SongTags__Container-sc-b55131f0-1 SEhjw'
MAX_THREADS = 6


def play_session() -> None:
    print('Welcome to Python DJ!')
    user_song = input('Please enter a Genius url to a song you like!\n')
    recommended = compare_songs_by_lyrics(user_song)
    print('Searching for similar songs...')

    for song in recommended:
        song_name, artist = song
        print(f'Check out {song_name} by {artist}!')


def get_song_lyrics(url: str) -> str:
    """
    This function scrapes the lyrics from the inputted URL.

    Parameter:
        url: A string that represents the genius.com URL of the song

    Return:
        A string that represents the lyrics of the song 
    """

    try:   
        response = rq.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        lyric_container = soup.select_one('div[data-lyrics-container="true"]').select_one('div[data-exclude-from-selection="true"]').decompose()
        lyric_container = soup.select_one('div[data-lyrics-container="true"]').get_text(separator= ' ')

        lyrics = re.split(r'\xa0', lyric_container)[0]
        if lyrics:
            return lyrics

    except AttributeError:
        return 'no lyrics'

def parse_song_links(song_info: tuple) -> tuple:
    """
    This is a wrapper function that returns a tuple of the song lyrics,
    song name, and the artist's name

    Parameter:
        song_info: A tuple containing the URL of the song, the song name, and
        the artist's name
    
    Return:
        A tuple that contains the song lyrics, song name, and artist name
    """

    song_url, song_name, song_artist = song_info

    song_lyrics = get_song_lyrics(song_url)

    return (song_lyrics, song_name, song_artist)

def compare_lyrics_similarity(song1: str, song2:str) -> int:
    """
    This function returns the similarity score between two songs by comparing
    the similarity between the nouns in each song

    Parameters:
        song1: A string containing the lyrics of the first song
        song2: A string containing the lyrics of the second song
    
    Return:
        A integer value between 0.0 and 1.0 that represents the similarity 
        of the two songs.
    """

    lyrics1 = nlp(song1)
    lyrics2 = nlp(song2)
    filtered_lyrics1 = nlp(' '.join([str(word) for word in lyrics1 if word.pos_ in ['NOUN', 'PROPN']]))
    filtered_lyrics2 = nlp(' '.join([str(word) for word in lyrics2 if word.pos_ in ['NOUN', 'PROPN']]))


    return filtered_lyrics1.similarity(filtered_lyrics2)


def get_song_genre(url:str) -> str:
    """
    This function identifies the genre of the inputted song

    Parameter:
        url: A string that represents the url of the song
    
    Returns:
        A string that represents the song's genre 
    """
    if 'genius' in url and 'lyrics' in url:
        response = rq.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        genre = soup.find('div', class_= SONG_TAGS_CONTAINER).contents[0].text
        return genre
    
    else:
        print('oopsies! you have inputted an unsupported link. try to upload a link from Genius.')



def get_similar_songs(target_genre:str) -> list[tuple]:
    """
    This function finds the similar songs based on the inputted genre

    Parameter:
        target_genre: A string that represents the genre that the user
        wants similar songs of
    
    Return:
        A list of tuples containing the song URL, song name, and artist
        name
    """

    similar_songs = []
    cache = set()
    with open('spotify_songs_final_filtered_6.csv', 'r', encoding='utf-8') as file:
        file.readline()

        while True:
            line = file.readline()
            if line == '':
                break
            
            song_information = line.split(',')
            
            song_genre = song_information[9]
            song_name = song_information[1]
        
            if (song_genre.lower() == target_genre.lower() and
                not re.search(r'\(.*?\)', song_name) and
                song_name not in cache):
                
                cache.add(song_name)
                song_artist = song_information[2]
                song_name = song_name.replace(' ', '-')
                song_artist = song_artist.replace(' ', '-')
                genius_url = f'https://www.genius.com/{song_artist}-{song_name}-lyrics'

                
                similar_songs.append((genius_url, song_name, song_artist))

        return similar_songs



def compare_songs_by_lyrics(url:str) -> list[tuple]:
    """
    This function returns five recommended songs based on the user's 
    inputted song

    Parameter:
        url: A string that represents the url of the song
    
    Returns:
        A list of tuples that contains the song name and the artist's name
    """

    recommended_songs = []

    user_song_lyrics = get_song_lyrics(url)
    target_genre = get_song_genre(url)
    similar_songs = get_similar_songs(target_genre)


    while len(recommended_songs) < 5:

        result = []
        for i in range(6):
            random_index = random.randrange(0, len(similar_songs))
            result.append(similar_songs.pop(random_index))

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            result = executor.map(parse_song_links,result)
        
        for song in result:
            song_lyrics, song_name, song_artist = song

            if compare_lyrics_similarity(user_song_lyrics, song_lyrics) > 0.8:
                recommended_songs.append((song_name, song_artist))
    
    return recommended_songs


play_session()




