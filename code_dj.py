import requests as rq
from bs4 import BeautifulSoup 



global common_phrases
common_phrases = set()



# response = rq.get('https://genius.com/Fugees-killing-me-softly-with-his-song-lyrics')

# soup = BeautifulSoup(response.text, 'html.parser')

# content_div = soup.find('div', class_='Lyrics__Container-sc-3d1d18a3-1 bjajog')

# split = content_div.text.split('Read More')

# with open('content.txt', 'w') as file:
#     file.write(split[1])

def setup() -> None:
    global common_phrases

    with open('words_to_avoid.csv', 'r') as file:
        word_list = file.readline().split(',')
        for word in word_list:
            common_phrases.add(word)
    
        

def scrap_lyrics(url: str) -> None:
    if 'genius.com' in url and 'lyrics' in url:    
        response = rq.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        lyric_text = soup.find('div', class_='Lyrics__Container-sc-3d1d18a3-1 bjajog').text
        lyric_text = lyric_text.split('Read More')[1]
        
        if lyric_text:
            with open('lyrics.txt', 'w', encoding='utf-8') as file:
                file.write(lyric_text)
    else:
        print('oopsies! you have inputted an unsupported link. try to upload a link from Genius.')



def record_word_count() -> None:

    

    return None


setup()

scrap_lyrics('https://genius.com/Kendrick-lamar-tv-off-lyrics')

