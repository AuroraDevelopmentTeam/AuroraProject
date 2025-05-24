import logging
import nextcord
from aurorabot.core.interfaces.error_handler import IErrorHandler
from aurorabot.core.exceptions import (
    CommandError,
    PermissionError,
    ArgumentError,
    ExecutionError,
    ValidationError
)


class ErrorHandlerService(IErrorHandler):
    """Сервис для обработки ошибок команд."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    async def handle_error(
        self,
        interaction: nextcord.Interaction,
        error: Exception
    ) -> None:
        """
        Обработка ошибки команды.
        
        Args:
            interaction: Объект взаимодействия с командой
            error: Объект ошибки
        """
        # Получаем сервис локализации из бота
        locale_service = interaction.client.locale_service
        
        if isinstance(error, CommandError):
            # Обработка ошибок команд
            await self._handle_command_error(interaction, error, locale_service)
        elif isinstance(error, PermissionError):
            # Обработка ошибок прав доступа
            await self._handle_permission_error(interaction, error, locale_service)
        elif isinstance(error, ArgumentError):
            # Обработка ошибок аргументов
            await self._handle_argument_error(interaction, error, locale_service)
        elif isinstance(error, ExecutionError):
            # Обработка ошибок выполнения
            await self._handle_execution_error(interaction, error, locale_service)
        elif isinstance(error, ValidationError):
            # Обработка ошибок валидации
            await self._handle_validation_error(interaction, error, locale_service)
        else:
            # Обработка неизвестных ошибок
            await self._handle_unknown_error(interaction, error, locale_service)

    async def _handle_command_error(
        self,
        interaction: nextcord.Interaction,
        error: CommandError,
        locale_service
    ) -> None:
        """Обработка ошибок команд."""
        await interaction.response.send_message(
            locale_service.get_text("common.error.command", error=str(error)),
            ephemeral=True
        )

    async def _handle_permission_error(
        self,
        interaction: nextcord.Interaction,
        error: PermissionError,
        locale_service
    ) -> None:
        """Обработка ошибок прав доступа."""
        await interaction.response.send_message(
            locale_service.get_text("common.error.permission", error=str(error)),
            ephemeral=True
        )

    async def _handle_argument_error(
        self,
        interaction: nextcord.Interaction,
        error: ArgumentError,
        locale_service
    ) -> None:
        """Обработка ошибок аргументов."""
        await interaction.response.send_message(
            locale_service.get_text("common.error.argument", error=str(error)),
            ephemeral=True
        )

    async def _handle_execution_error(
        self,
        interaction: nextcord.Interaction,
        error: ExecutionError,
        locale_service
    ) -> None:
        """Обработка ошибок выполнения."""
        await interaction.response.send_message(
            locale_service.get_text("common.error.execution", error=str(error)),
            ephemeral=True
        )

    async def _handle_validation_error(
        self,
        interaction: nextcord.Interaction,
        error: ValidationError,
        locale_service
    ) -> None:
        """Обработка ошибок валидации."""
        await interaction.response.send_message(
            locale_service.get_text("common.error.validation", error=str(error)),
            ephemeral=True
        )

    async def _handle_unknown_error(
        self,
        interaction: nextcord.Interaction,
        error: Exception,
        locale_service
    ) -> None:
        """Обработка неизвестных ошибок."""
        self.logger.error(f"Неизвестная ошибка: {error}", exc_info=True)
        await interaction.response.send_message(
            locale_service.get_text("common.error.unknown"),
            ephemeral=True
        ) 