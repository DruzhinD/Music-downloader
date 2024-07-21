import requests, fake_useragent #для доступа к сайту
from bs4 import BeautifulSoup, Tag
from song import Song
from converters import replace_symbols, time_to_seconds
import os

"""логика работы с данными из сети"""

#не может парсить больше 100 песен из плейлиста, т.к. страница прогружает именно столько.
#есть скрипт js, который подгружает оставшиеся песни, если их больше 100 в плейлисте
#но он пока не в учете
def get_yandex_playlist(ya_url: str) -> set[Song]:
    """Получение списка композиций по ссылке на плейлист яндекс музыки"""
    headers = {'User-Agent': fake_useragent.UserAgent(platforms='pc').random}
    response = requests.get(ya_url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    playlist_html = soup.find('div', class_='lightlist__cont') #тег, содержащий список всех композиций
    #список всех вложенных тегов div, в которых по отдельности находится единственная композиция
    track_elements = playlist_html.find_all("div", recursive=False)
    
    songs = set()
    #достаем название и автора
    for tag in track_elements:
        try:
            title = tag.find('div', class_='d-track__name').text.strip()
            artist = tag.find('div', class_='d-track__meta').text.strip()
            
            artist, title = replace_symbols(artist, title)

            #достаем длительность композиции
            duration_str = tag.find('div', class_='d-track__end-column').text.strip()
            duration = time_to_seconds(duration_str)

            songs.add(Song(title, artist, duration))
        except Exception as ex:
            continue

    return songs


def get_link_from_lightaudio(song: Song) -> str:
    """Получение ссылки на скачивание с сайта lightaudio"""

    base_url = 'https://web.ligaudio.ru/mp3/'

    #формируем запрос на сайт с разделителем %20
    url = base_url + '%20'.join(str(song).split(' '))
    headers = {'User-Agent': fake_useragent.UserAgent(platforms='pc').random}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')    
    #пытаемся прочитать количество композиций
    tracks_amount: int
    try:
        tag = soup.find('p', class_='foundnum').text.strip()
        tracks_amount = int(tag.split(' ')[1])
    except:
        raise ValueError(f'Не удалось найти {song} на web.ligaudio.ru')
    
    #рассмотрим не более 40 треков
    if tracks_amount > 40:
        tracks_amount = 40

    soup = soup.find('div', {'id': 'result'})
    tag: Tag = None #будет хранить в себе тег элемента, в котором хранится информация о композиции
    for i in range(tracks_amount):
        if tag != None:
            tag = tag.find_next_sibling('div')
        else:
            tag = soup.find('div')

        duration_str = tag.find('span', class_='d').text.strip()
        duration_find = time_to_seconds(duration_str)
        #0.13 = 13%, т.е. допустимая разница в длительности композиции на сайте и фактически полученной
        if song.duration * (1 - 0.13) < duration_find and duration_find < song.duration * (1 + 0.13):
            link = tag.find('a', class_='down').get('href')
            if not link.startswith('https:'):
                link = 'https:' + link
            return link          


def download_save_mp3(link: str, save_folder: str, song: Song) -> bool:
    """Загрузка и сохранение файла"""
    
    if os.path.exists(save_folder) == False:
        return False
    elif os.path.exists(f'{save_folder}\\{song}.mp3'):
        return False

    headers = {'User-Agent': fake_useragent.UserAgent(platforms='pc').random}
    response = requests.get(link, headers=headers)
    with open(f'{save_folder}/{song}.mp3', 'wb') as mp3_file:
        mp3_file.write(response.content)
    # print(f'{song} успешно сохранена!')
    return True
