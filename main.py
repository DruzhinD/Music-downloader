from typing import Union
from config import Config #класс конфигурации
from song import Song
import file_working as fw
import downloader as dwn
import os

"""файл запуска"""
def main():

    main_commands = {
        'ban': 'Добавить список песен-исключений',
        'show_ban': 'Просмотреть список песен-исключений',
        'load': 'Загрузить список песен для скачивания',
        'show_load': 'Просмотреть список песен для загрузки',
        'set_dir': 'Установить каталог для загрузки файлов',
        'show_dir': 'Просмотреть каталог для загрузки',
        'go': 'Начать загрузку',
        'exit': 'завершить работу'
    }

    config = Config() #конфигурация
    skip_songs: set[Song] = None
    if config.skip_list != None:
        skip_songs: set[Song] = set(config.skip_list) #список песен-исключений
    load_songs: set[Song] = None #список для скачивания
    save_dir: str = config.save_directory #каталог для сохранения

    while True:
        #очистка консоли
        #нужно сменить места для очистки консоли
        os.system('cls')
        print_commands(main_commands)
        com = input('Ввод: ')
        print('-'*10)
        if com == 'ban':
            #назначаем список композиций для пропуска
            skip_songs = get_skip_songs_list()
            if skip_songs != None:
                config.set_skip_list(list(skip_songs))

        elif com == 'show_ban':
            if skip_songs != None:
                print('Список исключений: ')
                for song in skip_songs:
                    print('\t' + str(song))
            else:
                print('Список пуст')

        elif com == 'load':
            load_songs = get_download_songs_list()

        elif com == 'show_load':
            if load_songs != None:
                print('Список для загрузки: ')
                for song in load_songs:
                    print('\t' + str(song))
            else:
                print('Список пуст')

        elif com == 'set_dir':
            temp_dir = set_download_folder()
            #назначаем директорию для сохранения
            if temp_dir != '':
                config.set_save_directory(temp_dir)
                save_dir = config.save_directory

        elif com == 'show_dir':
            print(f'Каталог для сохранения: {save_dir}')

        elif com == 'go':
            start_download(skip_songs, load_songs, save_dir)

        elif com == 'exit':
            print('Завершение работы программы...')
            break
        else:
            print('Команда не определена. Повторите ввод.')

        print('Для продолжения нажмите Enter')
        input('...')


def print_commands(command_list: dict) -> None:
    """Вывод в консоль доступных для ввода команд"""
    for key in command_list.keys():
        print(f'{key.ljust(10)}\t{command_list[key]}')

def get_skip_songs_list() -> Union[list[Song], None]:
    """Получение списка для игнорирования композиций"""

    ban_commands = {
        'txt': 'Добавить из текстового файла',
        'dir': 'Добавить список mp3 файлов из каталога',
        'exit': 'Вернуться в главное меню'
    }

    while True:
        print_commands(ban_commands)
        com = input('Ввод: ')
        if com == 'txt':
            com = input('Укажите путь к файлу: ')
            try:
                songs = fw.get_mp3_titles_from_file(com)
                return songs
            except FileNotFoundError as ex:
                print(ex)
                continue

        elif com == 'dir':
            com = input('Укажите путь к каталогу с mp3 файлами: ')
            try:
                mp3_paths = fw.get_mp3_paths_directory(com)
            except FileNotFoundError as ex:
                print(ex)
                continue
           
            songs = set()
            for path in mp3_paths:
                try:
                    song = Song.build_song_from_meta(path)
                    if song != None:
                        songs.add(song)
                except TypeError as ex:
                    print(ex)
                    continue
            if len(songs) > 0:
                return songs
            else:
                print('Не удалось добавить песни в исключения')

        elif com == 'exit':
            print('Возврат в главное меню...')
            return None
        else:
            print('Команда не определена. Повторите ввод.')
            continue

def get_download_songs_list() -> Union[list[Song], None]:
    """Получение списка композиций для скачивания"""

    load_commands = {
        'txt': 'Добавить из текстового файла',
        'yandex': 'Добавить из плейлиста яндекс музыки',
        'exit': 'Вернуться в главное меню'
    }

    while True:
        print_commands(load_commands)
        com = input('Ввод: ')
        if com == 'txt':
            com = input('Укажите путь к файлу: ')
            try:
                songs = fw.get_mp3_titles_from_file(com)
                return songs
            except FileNotFoundError as ex:
                print(ex)
                continue

        elif com == 'yandex':
            com = input('Укажите ссылку на плейлист яндекс музыки (плейлист должен быть общедоступным): ')

            #делаем несколько попыток получить список треков
            #возможно стоит убрать
            attempts = 3
            for i in range(attempts):
                try:
                    songs = dwn.get_yandex_playlist(com)
                    print(f'Список из {len(songs)} удачно сформирован.')
                    return songs
                except:
                    print(f'Попытка №{i+1} завершилась неудачно...')

        elif com == 'exit':
            print('Возврат в главное меню...')
            return None
        else:
            print('Команда не определена. Повторите ввод.')
            continue

def set_download_folder() -> str:
    """Установка каталога для загрузки"""
    
    save_dir = input('Введите путь к каталогу: ')
    if os.path.exists(save_dir) == False:
        print('Указанный каталог не найден')
        return ''
    return save_dir

def start_download(ban_list: set[Song], load_list: set[Song], save_folder: str):
    """Загрузка треков"""
    if save_folder == None:
        print('Не указан каталог для сохранения')
        return
    elif load_list == None:
        print('Не задан список для загрузки')
        return

    elif os.path.exists(save_folder) == False:
        raise FileNotFoundError('Указанный каталог не найден')
    
    #список треков, которые необходимо загрузить
    if ban_list != None:
        download_set = load_list - ban_list 
    elif load_list != None:
        download_set = load_list
    else:
        print('Список для загрузки не сформирован')
        return

    for song in download_set:
        try:
            link = dwn.get_link_from_lightaudio(song)
            if link != None:
                result = dwn.download_save_mp3(link, save_folder, song)               
            else:
                result = False
            if result == True:
                print(f'{song} успешно сохранена!')
            else:
                print(f'Не удалось загрузить {song}. Возможно она уже есть в этой папке.')

        except ValueError as ex:
            print(ex)
        except Exception as ex:
            print('Произошла неизвестная ошибка.')

        


if __name__ == '__main__':
    main()
