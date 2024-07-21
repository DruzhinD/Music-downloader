from typing import Tuple

"""Преобразование данных, т.е. конверторы"""

def replace_symbols(artist: str, title: str) -> Tuple[str, str]:
    """Заменяет запрещенные ОС символы на разрешенные в имени артиста и названии песни\n
    Возвращает artist, title"""
    #заменяем символы на допустимые
    ban = ['/', '\\', ':', '*', '"', '?', '>', '<', '|']
    for symb in ban:
        if artist.find(symb) != -1:
            artist = artist.replace(symb, '_')
        if title.find(symb) != -1:
            title = title.replace(symb, '_')
    return [artist, title]

def time_to_seconds(duration_str: str) -> int:
    """Подсчет количества секунд, исходя из строкового значения"""
    splited_duration: list = duration_str.split(':')
    splited_duration.reverse()
    duration: int = 0
    #подсчитываем количество секунд
    if len(splited_duration) <= 3:
        for i in range(len(splited_duration)):
            duration += int(splited_duration[i]) * (60**i)
    else:
        raise Exception('Композиция слишком длительная.')
    return duration

