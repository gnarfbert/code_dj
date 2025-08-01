import requests as rq
import spacy
from bs4 import BeautifulSoup 
from spacy.lang.en import stop_words


nlp = spacy.load("en_core_web_md")



LYRICS_CONTAINER = 'Lyrics__Container-sc-3d1d18a3-1 bjajog'
SONG_TAGS_CONTAINER = 'SongTags__Container-sc-b55131f0-1 SEhjw'


    
    
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



def compare_lyrics_similarity(song1: str, song2:str) -> int:
    lyrics1 = nlp(song1)
    lyrics2 = nlp(song2)
    filtered_lyrics1 = nlp(' '.join([str(word) for word in lyrics1 if not word.is_stop]))
    filtered_lyrics2 = nlp(' '.join([str(word) for word in lyrics2 if not word.is_stop]))


    return filtered_lyrics1.similarity(filtered_lyrics2)


def get_song_genre(url:str) -> str:

    if 'genius' in url and 'lyrics' in url:
        response = rq.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        genre = soup.find('div', class_= SONG_TAGS_CONTAINER).contents[0].text
        
        return genre
    
    else:
        print('oopsies! you have inputted an unsupported link. try to upload a link from Genius.')



def get_similar_songs(target_genre:str,target_artist:str) -> list:
    similar_songs = []
    with open('spotify_songs.csv', 'r', encoding= 'utf-8') as file:
        file.readline()

        while True:
            line = file.readline()
            if line == '':
                break
            
            song_information = line.split(',')
            
            song_genre = song_information[9]
            song_artist = song_information[2]

            if (song_genre.lower() == target_genre.lower() and 
                song_artist.lower() == target_artist.lower()):
                
                song_name = song_information[1]
                
                similar_songs.append((song_name, song_artist))

        return similar_songs



def compare_songs_by_lyrics(url:str) -> list:

    recommended_songs = []

    frequent_lyric_count = compare_lyrics_similarity(url)
    target_genre = get_song_genre(url)
    similar_songs = get_similar_songs(target_genre, 'drake')



    for song in similar_songs:

        song_name, song_artist = song

        song_artist = song_artist.replace(' ', '-')

        song_name = re.sub('\s*\(feat\..*?\)\s*', '',song_name).replace(' ', '-')

        query = f'https://www.genius.com/{song_artist}-{song_name}-lyrics'
        

        try:
            similar_song_lyrics = sorted(get_song_lyrics(query))
            frequent_lyric_count = sorted(frequent_lyric_count)


        except IndexError:
            continue
        except AttributeError:
            continue






    print(recommended_songs)





# print(record_word_count('https://genius.com/Clipse-so-be-it-lyrics'))

# print(get_song_genre('https://genius.com/Clipse-so-be-it-lyrics'))

# get_song_lyrics('https://genius.com/Clipse-so-be-it-lyrics')

# compare_songs_by_lyrics('https://genius.com/Clipse-so-be-it-lyrics')

# get_similar_songs('rap','drake')


compare_lyrics_similarity('hello he wants jimmy dinner', 'he went to china to get dumplings')




