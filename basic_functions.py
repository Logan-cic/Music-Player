import pygame
from pygame import mixer
import os
import eyed3
import io
from PIL import Image
import json
from tkinter import filedialog
import random
import copy

MUSIC_END = pygame.USEREVENT+1

START = 0

PLAYED_SONGS = []

NORMAL_ORDER = []

WHOLE_PLAYLIST = []

REPEAT_MODE = 0

NEXT_SONGS = []

INDEX = 0

CURRENT_PLAY_TIME = 0

RANDOM_MODE = True


def get_current_play_time():
    return CURRENT_PLAY_TIME


def get_start_time():
    return START


def load_song(song_path: str):
    """
    A função vai carregar e tocar a música especificada no diretório.
    :param song_path: diretório da música.
    :return: a duração total da música em segundos.
    """
    global CURRENT_PLAY_TIME
    global START
    global PLAYED_SONGS

    PLAYED_SONGS.append(song_path)
    START = 0
    mixer.music.load(song_path)
    mixer.music.play()
    CURRENT_PLAY_TIME = mixer.Sound(song_path).get_length()


def pause_song() -> None:
    mixer.music.pause()


def unpause_song() -> None:
    if not get_current_path():
        next_song()
    else:
        mixer.music.unpause()


def set_volume(volume: str) -> None:
    mixer.music.set_volume(float(volume))


def enqueue_song(song: str) -> None:
    global NEXT_SONGS
    NEXT_SONGS.append(song)


def end_song_to_next() -> str:
    global CURRENT_PLAY_TIME, NEXT_SONGS, PLAYED_SONGS, REPEAT_MODE
    mixer.music.set_endevent(MUSIC_END)
    for event in pygame.event.get():
        if event.type == MUSIC_END and len(NEXT_SONGS) > 0:
            if REPEAT_MODE == 2:
                load_song(PLAYED_SONGS[len(PLAYED_SONGS)-1])
                return PLAYED_SONGS[len(PLAYED_SONGS) - 1]
            elif REPEAT_MODE == 1 and not NEXT_SONGS:
                NEXT_SONGS.append(PLAYED_SONGS)
            song = NEXT_SONGS.pop(0)
            load_song(song)
            return song


def get_current_time() -> float:
    return mixer.music.get_pos() / 1000 + START


def set_time(start_time: float):
    global START
    START = start_time
    mixer.music.play(start=start_time)


def next_song() -> None:
    global NEXT_SONGS, CURRENT_PLAY_TIME, START, REPEAT_MODE

    if NEXT_SONGS:
        load_song(NEXT_SONGS.pop(0))
        START = 0
    elif not NEXT_SONGS and REPEAT_MODE == 1:
        print(NEXT_SONGS)
        for song in PLAYED_SONGS:
            NEXT_SONGS.append(song)
        load_song(NEXT_SONGS.pop(0))
        START = 0
    print(f"NEXT_SONGS = {NEXT_SONGS}")


def previous_song() -> None:
    global PLAYED_SONGS
    global NEXT_SONGS
    global CURRENT_PLAY_TIME

    played_size = len(PLAYED_SONGS) - 1
    if get_current_time() > 3:
        set_time(0)
    else:
        if played_size > 1:
            NEXT_SONGS.insert(0, PLAYED_SONGS.pop(played_size))
            played_size = len(PLAYED_SONGS) - 1
            song = PLAYED_SONGS.pop(played_size)
            load_song(song)


def get_songs_from_dir(directory: str) -> None:
    for song in os.listdir(directory):
        if song.endswith(".mp3"):
            enqueue_song(directory + "//" + song)


def get_album_cover():
    if get_current_path():
        path = get_current_path()
        song = eyed3.load(path)
        image = song.tag.images[0]
        image_data = image.image_data
        image = Image.open(io.BytesIO(image_data))
    else:
        image_data = r"Images\\default.png"
        image = Image.open(image_data)

    return image


def get_current_path() -> str:
    global PLAYED_SONGS

    if PLAYED_SONGS:
        return PLAYED_SONGS[len(PLAYED_SONGS) - 1]


def search_directory() -> None:
    folder = filedialog.askdirectory()
    add_song_folder(fr'{folder}')


def add_song_folder(path: str) -> None:
    with open("folders.json", 'r') as folders:
        json_object = json.load(folders)
    if json_object["folders"]:
        json_object["folders"].append(path)
    else:
        item = list()
        item.append(path)
        json_object["folders"] = item
    os.remove(r"folders.json")

    with open("folders.json", 'w') as folders:
        json.dump(json_object, folders)

    initialize_songs()


def initialize_songs() -> None:
    global INDEX

    index = INDEX
    with open("folders.json", "r") as json_file:
        json_data = json.load(json_file)
    print(json_data)
    if json_data["folders"]:
        for directory in range(index, len(json_data["folders"])):
            get_songs_from_dir(json_data["folders"][directory])
            INDEX = len(json_data)


def randomize_songs() -> None:
    global NORMAL_ORDER, NEXT_SONGS, PLAYED_SONGS, RANDOM_MODE, WHOLE_PLAYLIST
    if NORMAL_ORDER:
        index_wanted = WHOLE_PLAYLIST.index(PLAYED_SONGS[len(PLAYED_SONGS) - 1])
        NEXT_SONGS = copy.deepcopy(WHOLE_PLAYLIST[index_wanted + 1:])
        NORMAL_ORDER = []
        RANDOM_MODE = False
        print(f"NORMAL_ORDER = {NORMAL_ORDER}")
    else:
        NORMAL_ORDER = copy.deepcopy(NEXT_SONGS)
        if not WHOLE_PLAYLIST:
            if not PLAYED_SONGS:
                WHOLE_PLAYLIST = copy.deepcopy(NORMAL_ORDER)
            else:
                WHOLE_PLAYLIST = PLAYED_SONGS + NORMAL_ORDER
        if not NEXT_SONGS:
            NEXT_SONGS = PLAYED_SONGS[:len(PLAYED_SONGS)-1]
            print("1")
        else:
            print("2")
            print(NEXT_SONGS)
            # NEXT_SONGS.append(PLAYED_SONGS[:len(PLAYED_SONGS)-1])
            for song in range(0, len(PLAYED_SONGS)-1):
                NEXT_SONGS.append(PLAYED_SONGS[song])

        random.shuffle(NEXT_SONGS)
        RANDOM_MODE = True
    print(f"WHOLE_PLAYLIST = {WHOLE_PLAYLIST}")
    print(f"NEXT_SONGS = {NEXT_SONGS}")


def get_random_mode() -> bool:
    return RANDOM_MODE


def repeat_songs() -> None:
    global PLAYED_SONGS, WHOLE_PLAYLIST, REPEAT_MODE, NEXT_SONGS

    if REPEAT_MODE == 2:
        REPEAT_MODE = 0
        index_wanted = WHOLE_PLAYLIST.index(PLAYED_SONGS[len(PLAYED_SONGS) - 1])
        # NEXT_SONGS = copy.deepcopy(WHOLE_PLAYLIST[index_wanted + 1:])
        NEXT_SONGS = []
        for song in range(index_wanted + 1, len(WHOLE_PLAYLIST)-1):
            NEXT_SONGS.append(WHOLE_PLAYLIST[song])
        WHOLE_PLAYLIST = []
    elif REPEAT_MODE == 1:
        REPEAT_MODE = 2
    else:
        if not WHOLE_PLAYLIST:
            WHOLE_PLAYLIST = PLAYED_SONGS + NEXT_SONGS
        # NEXT_SONGS.append(PLAYED_SONGS)
        for song in PLAYED_SONGS:
            NEXT_SONGS.append(song)
        REPEAT_MODE = 1
    print(NEXT_SONGS)


def get_repeat_mode() -> int:
    return REPEAT_MODE


if __name__ == "__main__":
    pygame.init()

    search_directory()
