import nextcord
from typing import Optional, Dict, Any


def create_base_embed(
    title: str,
    color: nextcord.Color = nextcord.Color.blue(),
    thumbnail_url: Optional[str] = None,
    footer_text: Optional[str] = None,
    footer_icon: Optional[str] = None
) -> nextcord.Embed:
    """Create a base embed with common properties."""
    embed = nextcord.Embed(title=title, color=color)
    
    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)
        
    if footer_text:
        embed.set_footer(text=footer_text, icon_url=footer_icon)
        
    return embed


def add_fields(embed: nextcord.Embed, fields: Dict[str, Any]) -> nextcord.Embed:
    """Add multiple fields to an embed."""
    for name, value in fields.items():
        embed.add_field(
            name=name,
            value=str(value) if value is not None else "N/A",
            inline=True
        )
    return embed 