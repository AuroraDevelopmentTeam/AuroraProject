from abc import ABC, abstractmethod
import nextcord


class IErrorHandler(ABC):
    """Интерфейс для обработчиков ошибок."""

    @abstractmethod
    async def handle_error(
        self,
        interaction: nextcord.Interaction,
        error: Exception
    ) -> None:
        """
        Обработка ошибки.
        
        Args:
            interaction: Объект взаимодействия с командой
            error: Объект ошибки
        """
        pass 