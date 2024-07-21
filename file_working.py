from typing import Union
import os
from song import Song

"""Работа с файлами"""

def get_mp3_paths_directory(directory_path: str) -> list[str]:
    """Поиск mp3 файлов, которые есть в директории \n
    Возвращает список путей к этим файлам"""
    
    if os.path.exists(directory_path) == False:
        raise FileNotFoundError('Не удалось найти указанный каталог')
    
    mp3_paths = []
    for root, dirs, files in os.walk(directory_path, followlinks=False):
        for file in files:
            if file.endswith('.mp3'):
                mp3_paths.append(f'{root}\\{file}')
    return mp3_paths

def get_mp3_titles_from_file(file_path) -> Union[set[Song], None]:
    """обрабатывает строки из файла в формате: 'артист - название - 0:00 (длительность)' \n
    Если файл удалось открыть, то возвращает список композиций, иначе None"""
    
    if os.path.exists(file_path) == False:
        raise FileNotFoundError('Не удалось найти файл')
        
    songs = set()
    with open(file_path, 'r') as file:
        row = ' '
        while row != '':
            row = file.readline()
            try:
                song = Song.build_song_from_string(row)
                songs.add(song)
            except Exception as ex:
                continue

    return songs

