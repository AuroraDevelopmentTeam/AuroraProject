"""Модуль с пользовательскими исключениями."""

class CommandError(Exception):
    """Базовый класс для ошибок команд."""
    pass


class PermissionError(CommandError):
    """Ошибка прав доступа."""
    pass


class ArgumentError(CommandError):
    """Ошибка аргументов команды."""
    pass


class ExecutionError(CommandError):
    """Ошибка выполнения команды."""
    pass


class ValidationError(CommandError):
    """Ошибка валидации данных."""
    pass 