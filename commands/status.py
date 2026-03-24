import discord
from discord.ext import commands
from discord import app_commands

from utils import scrapper
from config import links

class Status(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    async def status(self, ctx_or_interaction):

        # Função que roda quando o usuário seleciona uma opção
        async def select_callback(interaction: discord.Interaction):
            choice = interaction.data['values'][0]
            await interaction.response.send_message(f'Calma ai kk, ainda não foi implementado, mas é uma boa ideia!')
        
        selections = discord.ui.Select(placeholder='Selecione uma opção')
        options = [
            discord.SelectOption(label='Jira', value='jira'),
            discord.SelectOption(label='Github', value='github'),
            discord.SelectOption(label='Sefaz', value='sefaz')
        ]
        selections.options = options
        selections.callback = select_callback
        
        view = discord.ui.View()

        view.add_item(selections)

        embed_message = discord.Embed(
            title=f'Verificar Status',
            description='Selecione uma opção para verificar o status',
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )

        if isinstance(ctx_or_interaction, discord.Interaction):
            await ctx_or_interaction.response.send_message(embed=embed_message, view=view)
        else:
            await ctx_or_interaction.send(embed=embed_message, view=view)
    
    @commands.command(name='status', description='Verifica o status de algumas APIs')
    async def status_prefix(self, ctx: commands.Context):
        await self.status(ctx)
    
    @app_commands.command(name='status', description='Verifica o status de algumas APIs')
    async def status_slash(self, interaction: discord.Interaction):
        await self.status(interaction)

async def setup(bot):
    await bot.add_cog(Status(bot))