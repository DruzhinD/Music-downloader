from mutagen import File
from converters import replace_symbols, time_to_seconds

class Song():
    """объект композиции/песни"""
    def __init__(self, artist: str, title: str, duration: int) -> None:
        self.artist = artist
        self.title = title
        self.duration = duration #длительность в секундах
    def __str__(self) -> str:
        return f'{self.artist} - {self.title}'
    
    @staticmethod
    def build_song_from_meta(mp3_path: str) -> object:
        """Получение автора и названия трека из файлов mp3\n
        Возврат Song"""
        try:
            # audio = EasyID3(mp3_path)
            # artist: str = audio['artist'][0]
            # title = audio['title'][0]
            # audio = MP3(mp3_path)
            # duration = int(audio.info.length)

            audio = File(mp3_path)
            artist = audio.get("TPE1").text[0]
            title = audio.get("TIT2").text[0]
            duration = int(audio.info.length)                       
            #заменяем символы на допустимые
            artist, title = replace_symbols(artist, title)
            return Song(artist, title, duration)
        
        except Exception as ex:
            raise TypeError(f'Не удалось получить информацию о композиции по пути: "{mp3_path}"')
            
    def __eq__(self, __value: object) -> bool:
        if __value == None:
            return False
        return (self.artist.lower().find(__value.artist.lower()) != -1 and 
                self.title.lower().find(__value.title.lower()) != -1 )
    def __hash__(self) -> int:
        return hash(str(self))
    
    @staticmethod
    def build_song_from_string(mp3_str: str) -> object:
        """Парсинг строки и создание объекта Song\n
        обрабатывает строки из файла в формате 'артист - название - 0:00 (длительность)'"""

        splited_str = mp3_str.split(' - ')
        if len(splited_str) != 3:
            raise ValueError("Неверный формат строки")
               
        artist = splited_str[0]
        title = splited_str[1]
        try:
            duration = time_to_seconds(splited_str[2])
            return Song(artist, title, duration)
        except Exception as ex:
            raise ValueError(ex)
    
    def to_json(obj) -> dict:
        """сериализация в json"""
        if isinstance(obj, Song):
            result = obj.__dict__
            return result
    
    @staticmethod
    def from_json(obj: dict) -> object:
        """десериализация объекта из json
        Возврат Song"""
        artist = obj['artist']
        title = obj['title']
        duration = obj['duration']
        return Song(artist, title, duration)