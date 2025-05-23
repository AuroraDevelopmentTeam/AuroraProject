from abc import ABC, abstractmethod
import nextcord
from nextcord.ext import commands
from typing import Optional, List, Any, Dict


class BaseInformationCommand(ABC):
    """Base class for all information-related commands."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @abstractmethod
    async def create_embed(self, ctx: commands.Context, **kwargs) -> nextcord.Embed:
        """Create the embed for the command."""
        pass

    @abstractmethod
    async def gather_information(self, **kwargs) -> Dict[str, Any]:
        """Gather the information needed for the command."""
        pass

    async def send_embed(self, ctx: commands.Context, **kwargs) -> None:
        """Send the embed to the channel."""
        embed = await self.create_embed(ctx, **kwargs)
        await ctx.send(embed=embed)

    def format_field(self, name: str, value: Any, inline: bool = True) -> Dict[str, Any]:
        """Format a field for the embed."""
        return {
            "name": name,
            "value": str(value) if value is not None else "N/A",
            "inline": inline
        }
