import os

from vk_api import VkApi
from json import loads
from re import match
import requests
import subprocess
from vaud import decode
from lib.vk_audio.exc import *
from discord import Embed, Color
from os import mkdir, rmdir
from os.path import exists


class Audio:
    # Не совсем понятно, что это за id. Но пусть будут id песни и owner_id
    _SONG_ID = 1
    _OWNER_ID = 0

    _SONG_NAME = 3
    _ARTIST_NAME = 4
    _IMG_URL = 14

    def __init__(self, audio_dict):
        self._json_parse(audio_dict)

    def _json_parse(self, audio_dict):
        self.name = audio_dict[self._SONG_NAME]
        self.artist_name = audio_dict[self._ARTIST_NAME]
        self.id = f'{audio_dict[self._SONG_ID]}_{audio_dict[self._OWNER_ID]}'

        self.hash = None
        for el in audio_dict:
            if isinstance(el, str) and match(r'\w+//\w+///\w+/', el):

                el = el.strip('/')
                while '//' in el:
                    el = el.replace('//', '/')
                el = el.split('/')

                self.hash = f'{self.id}_{el[1]}_{el[2]}'
                break
        if self.hash is None:
            raise AudioNotAvailable()

        self.img_url = audio_dict[self._IMG_URL].split(',')[-1]
        if not self.img_url.startswith('https://'):
            self.img_url = None

    def get_discord_embed(self, title, requester):
        embed = Embed(title=title,
                      description=self.artist_name,
                      color=Color.red())

        if self.img_url:
            embed.set_image(url=self.img_url).add_field(name="Track:",
                                                        value=f'[{self.name}](https://vk.com/audio{self.id})')
        else:
            embed.add_field(name="Track:", value=self.name)

        embed.add_field(name='Requested by', value=requester.mention)

        return embed

    @property
    def dir(self):
        tmp_file = 'tmp'
        return f'{tmp_file}/{self.id}'

    @property
    def path(self):
        return f'{self.dir}/audio.mp3'

    def __repr__(self):
        return f'{self.artist_name} - {self.name}'


class VkAudio:
    _id = None

    def __init__(self, vk_sess: VkApi):
        self.vk_sess = vk_sess

    def get_song_id_by_name(self, query_string: str) -> Audio:
        data = {'act': 'section',
                'al': 1, 'claim': 0, "is_layer": 0,  # Какие-то параметры
                "owner_id": self.user_id,
                "q": query_string,
                "section": 'search'}
        resp = self.vk_sess.http.post('https://vk.com/al_audio.php?act=section', data=data)
        assert resp.status_code == 200
        resp_json = loads(resp.text.strip('<!--'))

        try:
            song_data = resp_json['payload'][1][1]['playlist']['list'][0]
        except TypeError:
            raise AudioNotFoundException()

        audio = Audio(song_data)
        return audio

    def download_song_by_name(self, song_name) -> Audio:
        audio = self.get_song_id_by_name(song_name)

        if exists(audio.path):
            return audio

        data = {"al": 1, "ids": audio.hash}
        resp = self.vk_sess.http.post('https://vk.com/al_audio.php?act=reload_audio', data=data)
        assert resp.status_code == 200

        resp_json = loads(resp.text.strip('<!--'))
        url = decode(self.user_id, resp_json['payload'][1][0][0][2]).rstrip('/index.m3u8')
        print(url)

        try:
            mkdir(audio.dir)
        except FileExistsError:
            rmdir(audio.dir)
            mkdir(audio.dir)

        resp = requests.get(url + '/key.pub')
        print(resp.url)
        assert resp.status_code == 200
        with open(f'{audio.dir}/key.pub', 'w') as f:
            f.write(resp.text)

        resp = requests.get(url + '/index.m3u8')
        assert resp.status_code == 200
        m3u8 = resp.text.split('\n')

        for index, string in enumerate(m3u8):
            if string.startswith('seg'):
                resp = requests.get(f'{url}/{string}')
                assert resp.status_code == 200

                with open(f'{audio.dir}/{string}', 'wb') as f:
                    f.write(resp.content)
            elif 'URI' in string:
                m3u8[index] = m3u8[index].split('"')[0] + 'key.pub'

        with open(f'{audio.dir}/index.m3u8', 'w') as f:
            f.write('\n'.join(m3u8))

        subprocess.call(f'/usr/bin/ffmpeg -y -allowed_extensions ALL -i {audio.dir}/index.m3u8 -c copy {audio.path}', shell=True)

        return audio

    @property
    def user_id(self):
        if self._id is None:
            self._id = self.vk_sess.method("users.get")[0]["id"]
        return self._id

    def vk_auth(self):
        self.vk_sess.auth()
