from typing import Dict, Any, List, Optional, Tuple, Union
import nextcord


class FieldManager:
    """Manages the addition and formatting of fields in Discord embeds."""

    @staticmethod
    def format_field(
            name: str,
            value: Any,
            inline: bool = True
    ) -> Dict[str, Any]:
        """Format a single field for an embed."""
        return {
            "name": name,
            "value": FieldManager.format_field_value(value) if value is not None else "N/A",
            "inline": inline
        }

    @staticmethod
    def add_fields(
            embed: nextcord.Embed,
            fields: List[Tuple[str, str, bool]]
    ) -> nextcord.Embed:
        """
        Добавляет поля в эмбед.

        Args:
            embed: Эмбед, в который добавляются поля
            fields: Список кортежей (имя, значение, inline)
        """
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        return embed

    @staticmethod
    def add_field_list(
            embed: nextcord.Embed,
            fields: List[Dict[str, Any]]
    ) -> nextcord.Embed:
        """Add a list of pre-formatted fields to an embed."""
        for field in fields:
            embed.add_field(**field)
        return embed

    @staticmethod
    def format_field_value(value: Union[str, int, float, bool]) -> str:
        """
        Форматирует значение поля для отображения в эмбеде.

        Args:
            value: Значение для форматирования

        Returns:
            str: Отформатированное значение
        """
        if isinstance(value, bool):
            return "Да" if value else "Нет"
        return str(value)

    @staticmethod
    def format_list(items: List[str], bullet: str = "•") -> str:
        """
        Форматирует список элементов в строку с маркерами.

        Args:
            items: Список элементов
            bullet: Символ маркера

        Returns:
            str: Отформатированная строка
        """
        return "\n".join(f"{bullet} {item}" for item in items)

    @staticmethod
    def format_code_block(content: str, language: str = "") -> str:
        """
        Форматирует текст как блок кода.

        Args:
            content: Текст для форматирования
            language: Язык программирования для подсветки синтаксиса

        Returns:
            str: Отформатированный блок кода
        """
        return f"```{language}\n{content}\n```"
