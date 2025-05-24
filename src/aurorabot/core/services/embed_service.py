from typing import Any, Dict, Optional, List, Union
import nextcord
from aurorabot.core.embeds.builder import EmbedBuilder
from aurorabot.core.embeds.fields import FieldManager


class EmbedService:
    """Service for creating and managing embeds."""
    
    def create_embed(
        self,
        title: str,
        description: Optional[str] = None,
        color: Optional[Union[nextcord.Color, int]] = None,
        url: Optional[str] = None,
        thumbnail: Optional[str] = None,
        image: Optional[str] = None,
        footer_text: Optional[str] = None,
        footer_icon: Optional[str] = None,
        timestamp: Optional[bool] = True
    ) -> nextcord.Embed:
        """Create a new embed."""
        embed = nextcord.Embed(
            title=title,
            description=description,
            color=color or nextcord.Color.blue(),
            url=url
        )
        
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
            
        if image:
            embed.set_image(url=image)
            
        if footer_text:
            embed.set_footer(text=footer_text, icon_url=footer_icon)
            
        if timestamp:
            embed.timestamp = nextcord.utils.utcnow()
            
        return embed
        
    def add_fields(
        self,
        embed: nextcord.Embed,
        fields: Dict[str, Any],
        inline: bool = True
    ) -> nextcord.Embed:
        """Add fields to an embed."""
        for name, value in fields.items():
            if value is not None:
                embed.add_field(
                    name=name,
                    value=str(value),
                    inline=inline
                )
        return embed
        
    def add_field(
        self,
        embed: nextcord.Embed,
        name: str,
        value: Any,
        inline: bool = True
    ) -> nextcord.Embed:
        """Add a single field to an embed."""
        if value is not None:
            embed.add_field(
                name=name,
                value=str(value),
                inline=inline
            )
        return embed
    
    @staticmethod
    def format_field(name: str, value: Any, inline: bool = True) -> Dict[str, Any]:
        """Format a field for the embed."""
        return {
            "name": name,
            "value": str(value) if value is not None else "N/A",
            "inline": inline
        } 