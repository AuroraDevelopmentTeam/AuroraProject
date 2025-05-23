import nextcord
from typing import Optional, Union


class EmbedBuilder:
    def __init__(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        color: Optional[Union[nextcord.Color, int]] = None,
        url: Optional[str] = None
    ):
        """
        Создает новый экземпляр EmbedBuilder.

        Args:
            title: Заголовок эмбеда
            description: Описание эмбеда
            color: Цвет эмбеда (nextcord.Color или целое число)
            url: URL для заголовка эмбеда
        """
        self.embed = nextcord.Embed(
            title=title,
            description=description,
            color=color or nextcord.Color.blue(),
            url=url
        )

    def with_author(
        self,
        name: str,
        icon_url: Optional[str] = None,
        url: Optional[str] = None
    ) -> 'EmbedBuilder':
        """
        Добавляет информацию об авторе в эмбед.

        Args:
            name: Имя автора
            icon_url: URL иконки автора
            url: URL автора

        Returns:
            self: Текущий экземпляр EmbedBuilder для цепочки вызовов
        """
        self.embed.set_author(name=name, icon_url=icon_url, url=url)
        return self

    def with_footer(
        self,
        text: str,
        icon_url: Optional[str] = None
    ) -> 'EmbedBuilder':
        """
        Добавляет подпись в эмбед.

        Args:
            text: Текст подписи
            icon_url: URL иконки подписи

        Returns:
            self: Текущий экземпляр EmbedBuilder для цепочки вызовов
        """
        self.embed.set_footer(text=text, icon_url=icon_url)
        return self

    def with_thumbnail(self, url: str) -> 'EmbedBuilder':
        """
        Добавляет миниатюру в эмбед.

        Args:
            url: URL миниатюры

        Returns:
            self: Текущий экземпляр EmbedBuilder для цепочки вызовов
        """
        self.embed.set_thumbnail(url=url)
        return self

    def with_image(self, url: str) -> 'EmbedBuilder':
        """
        Добавляет изображение в эмбед.

        Args:
            url: URL изображения

        Returns:
            self: Текущий экземпляр EmbedBuilder для цепочки вызовов
        """
        self.embed.set_image(url=url)
        return self

    def with_timestamp(self, timestamp: Optional[float] = None) -> 'EmbedBuilder':
        """
        Добавляет временную метку в эмбед.

        Args:
            timestamp: Временная метка (если None, используется текущее время)

        Returns:
            self: Текущий экземпляр EmbedBuilder для цепочки вызовов
        """
        self.embed.timestamp = timestamp
        return self

    def build(self) -> nextcord.Embed:
        """
        Создает и возвращает готовый эмбед.

        Returns:
            nextcord.Embed: Готовый эмбед
        """
        return self.embed 