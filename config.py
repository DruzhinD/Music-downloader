import os
import json
from song import Song

class Config():
    """класс конфигурации"""
    def __init__(self) -> None:
        self.save_directory: str = 'data/loaded'
        self.skip_list: list[Song] = None
        self.config_path: str = 'data/config.json'

        #проверяем существование каталога с данными
        if not os.path.exists('data'):
            os.mkdir('data')
        
        #проверяем существование файла с конфигурацией
        if not os.path.exists(self.config_path):
            #создаем каталог под музыку
            if not os.path.exists(self.save_directory):
                os.mkdir('data/loaded')
            file = open(self.config_path, 'w')
            data: dict = {
                'save_directory': self.save_directory,
                'skip_list': [],
            }
            json_data = json.dumps(data)
            file.write(json_data)
            file.close()
        
        #загружаем конфигурацию из существующего файла
        else:
            file = open(self.config_path, 'r')
            data = file.readlines()
            loaded_dict = json.loads(' '.join(data))
            file.close()

            self.save_directory = loaded_dict['save_directory']

            #преобразуем объекты из dict в Song
            songs = []
            for song in loaded_dict['skip_list']:
                songs.append(Song.from_json(song))

            self.skip_list = songs

    def set_skip_list(self, skip_list: list[Song]):
        """Установка песен-исключений для загрузки"""
        file = open(self.config_path, 'r')
        data = file.readlines()
        loaded_dict = json.loads(' '.join(data))
        file.close()

        songs_dicted_list = []
        for song in skip_list:
            songs_dicted_list.append(song.to_json())
        loaded_dict['skip_list'] = songs_dicted_list
        json_data = json.dumps(loaded_dict)
        file = open(self.config_path, 'w')
        file.write(json_data)
        file.close()

        self.skip_list = skip_list
    
    def set_save_directory(self, save_directory: str):
        file = open(self.config_path, 'r')
        data = file.readlines()
        loaded_dict = json.loads(' '.join(data))
        file.close()

        loaded_dict['save_directory'] = save_directory

        json_data = json.dumps(loaded_dict)
        file = open(self.config_path, 'w')
        file.write(json_data)
        file.close()

        self.save_directory = save_directory