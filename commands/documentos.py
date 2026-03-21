import discord
from discord.ext import commands
from discord import app_commands

from utils import scrapper
from config import links

class Documentos(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    async def documentos_fiscais(self, ctx_or_interaction):

        # Função que roda quando o usuário seleciona uma opção
        async def select_callback(interaction: discord.Interaction):
            choice = interaction.data['values'][0]
            valor = scrapper.buscar_notas(choice, links.URLS_FISCAIS[choice])

            embed_message = discord.Embed(
                title=f'Documentos Fiscais - {choice}',
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow()
            )

            for i in valor:
                embed_message.add_field(name=i['texto'], value=i['url'], inline=False)

            # Configuração da view de resposta
            view_resultado = discord.ui.View()

            # Botão de Callback
            async def download_callback(interaction: discord.Interaction):
                await interaction.response.send_message("Preparando download...", ephemeral=True)
                import io
                buffer = io.StringIO(str(valor))
                file = discord.File(fp=buffer, filename=f"documentos_{choice}.txt")
                await interaction.followup.send(file=file, ephemeral=True)

            btn_download = discord.ui.Button(label='Baixar Documentos', style=discord.ButtonStyle.success)
            btn_download.callback = download_callback
            
            # Botão de Link
            btn_link = discord.ui.Button(label='Ir para Portal', style=discord.ButtonStyle.link, url=links.URLS_FISCAIS[choice])

            view_resultado.add_item(btn_download)
            view_resultado.add_item(btn_link)

            await interaction.response.send_message(embed=embed_message, view=view_resultado)
        
        selections = discord.ui.Select(placeholder='Selecione uma opção')
        options = [
            discord.SelectOption(label='NFe', value='NFe'),
            discord.SelectOption(label='NFCe', value='NFCe'),
            discord.SelectOption(label='CTe', value='CTe'),
            discord.SelectOption(label='MDFe', value='MDFe')
        ]
        selections.options = options
        selections.callback = select_callback
        
        view = discord.ui.View()

        view.add_item(selections)
        if isinstance(ctx_or_interaction, discord.Interaction):
            await ctx_or_interaction.response.send_message(view=view)
        else:
            await ctx_or_interaction.send(view=view)
    
    @commands.command(name='documentos', description='Busca documentos fiscais')
    async def documentos_prefix(self, ctx: commands.Context):
        await self.documentos_fiscais(ctx)
    
    @app_commands.command(name='documentos', description='Busca documentos fiscais')
    async def documentos_slash(self, interaction: discord.Interaction):
        await self.documentos_fiscais(interaction)

async def setup(bot):
    await bot.add_cog(Documentos(bot))