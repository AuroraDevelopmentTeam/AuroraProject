import textwrap
from vk_api import VkApi
from vk_api import audio as vka
from config import settings
import wavelink
from wavelink.ext import spotify
from core.utils import format_seconds_to_hhmmss


class Search(): 
    """Описание поиска и его функций"""
    def __init__(self, query: str):
        """Записываем запрос в свойства"""
        self.query = query

    def check_platform(self, query: str):
        """Проверить платформу запроса"""
        if query.startswith('http://') or query.startswith('https://'):
            if 'vk.com' in query:
                return 'vk'
            elif 'youtube.com' in query or 'youtu.be' in query:
                return 'yt'
            elif 'spotify.com' in query:
                return 'sp'
            else:
                return 'err'
        else:
            return 'search'

    def search(self):
        platform = self.check_platform(self.query)

        async def vksearch(query: str):
            vksess = VkApi(settings['vklogin'], settings['vkpass'])
            vksess.auth()
            splited_url = query.split('audio_playlist')
            temp_data = splited_url[1].split('_')
            owner_id = temp_data[0]
            temp_data = temp_data[1].split('%2F')
            album_id = temp_data[0]
            access_hash = temp_data[1]
            return vka.VkAudio(vksess).get(owner_id, album_id, access_hash)

        async def ytsearch(query: str):
            return await wavelink.YouTubeTrack.search(query=query)
        
        async def spsearch(query: str):
            return await spotify.SpotifyTrack.search(query=query)

        async def text_search(query: str):
            tracks = await wavelink.YouTubeTrack.search(query="music", return_first=False)
            auto = []
            for track in tracks:
                title = textwrap.shorten(track.title, width=75, placeholder="...")
                duration = format_seconds_to_hhmmss(track.duration)
                if duration[:3] == "00:":
                    duration = duration[3:]
                auto.append(f"{title} ({duration})")
            return auto
            
        async def get_results(query=self.query):
            platform = self.check_platform(query)
            #if platform ==
