from abc import ABC, abstractmethod
from typing import Any, Dict
import nextcord
from nextcord.ext import commands


class ICommand(ABC):
    """Interface for all bot commands."""
    
    @abstractmethod
    async def execute(self, interaction: nextcord.Interaction, **kwargs) -> None:
        """Execute the command."""
        pass


class IInformationCommand(ICommand):
    """Interface for information-related commands."""
    
    @abstractmethod
    async def gather_information(self, **kwargs) -> Dict[str, Any]:
        """Gather information needed for the command."""
        pass

    @abstractmethod
    async def create_embed(self, interaction: nextcord.Interaction, **kwargs) -> nextcord.Embed:
        """Create the embed for the command."""
        pass 