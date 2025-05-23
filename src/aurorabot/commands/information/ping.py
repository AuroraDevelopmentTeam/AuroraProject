import time
import nextcord
from nextcord.ext import commands
from aurorabot.core.base.information import BaseInformationCommand
from aurorabot.core.embeds.builder import EmbedBuilder
from aurorabot.core.embeds.fields import FieldManager


class PingCommand(BaseInformationCommand):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    async def gather_information(self, **kwargs) -> dict:
        """Gather ping information."""
        start_time = time.time()
        message = kwargs.get('message')
        end_time = time.time()
        
        return {
            'bot_latency': round((end_time - start_time) * 1000),
            'api_latency': round(self.bot.latency * 1000),
            'message': message
        }

    async def create_embed(self, ctx: commands.Context, **kwargs) -> nextcord.Embed:
        """Create the ping embed."""
        info = await self.gather_information(**kwargs)
        
        fields = {
            "Задержка бота": f"{info['bot_latency']}мс",
            "Задержка API": f"{info['api_latency']}мс"
        }
        
        embed = (
            EmbedBuilder("🏓 Понг!", color=nextcord.Color.green())
            .with_footer(f"Запрошено пользователем {ctx.author}", ctx.author.display_avatar)
            .build()
        )
        
        return FieldManager.add_fields(embed, fields)

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        """Проверяет задержку бота и API Discord."""
        # Создание эмбеда
        embed = EmbedBuilder(
            title="🏓 Понг!",
            color=nextcord.Color.green()
        ).build()

        # Получение задержки
        latency = round(self.bot.latency * 1000)
        
        # Добавление полей
        fields = [
            ("Задержка бота", f"{latency}мс", True),
            ("Задержка API", "Загрузка...", True)
        ]
        
        FieldManager.add_fields(embed, fields)
        
        # Отправка сообщения
        message = await ctx.send(embed=embed)
        
        # Обновление задержки API
        api_latency = round((message.created_at - ctx.message.created_at).total_seconds() * 1000)
        embed.set_field_at(1, name="Задержка API", value=f"{api_latency}мс", inline=True)
        
        await message.edit(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PingCommand(bot)) 