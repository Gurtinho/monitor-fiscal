import discord
from discord.ext import commands
from discord import app_commands

from utils import scrapper
from config import links
from utils import download

class Documentos(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    async def documentos_fiscais(self, ctx_or_interaction):

        # Função que roda quando o usuário seleciona uma opção
        async def select_callback(interaction: discord.Interaction):
            choice = interaction.data['values'][0]
            notas = scrapper.buscar_notas(choice)

            quantidade_notas = len(notas['documentos'])

            embed_message = discord.Embed(
                title=f'Documentos Fiscais - {choice}',
                description=f'Quantidade de documentos encontrados: {quantidade_notas}',
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow()
            )

            if notas['documentos']:
                for i in notas['documentos']:
                    embed_message.add_field(name=i['texto'], value=i['url'], inline=False)
            else:
                embed_message.add_field(name='Aviso', value='Nenhum documento encontrado!', inline=False)
                embed_message.add_field(name='Status', value='Pode ficar suave e tomar seu café ☕', inline=False)

            # Configuração da view de resposta
            view_resultado = discord.ui.View()

            # Botão de download dos arquivos
            async def download_callback(btn_interaction: discord.Interaction):
                await btn_interaction.response.send_message("📦 Preparando pacotinho ZIP...", ephemeral=True)
                file = download.zipar(notas['documentos'], choice)
                await btn_interaction.followup.send(content="Aqui estão os arquivos:", file=file, ephemeral=True)

            btn_download = discord.ui.Button(label='Baixar Documentos', style=discord.ButtonStyle.success)
            btn_download.callback = download_callback
            
            # Botão de link
            btn_link = discord.ui.Button(label='Ir para Portal', style=discord.ButtonStyle.link, url=notas['url_portal'])

            view_resultado.add_item(btn_download)
            view_resultado.add_item(btn_link)

            await interaction.response.edit_message(embed=embed_message, view=view_resultado)
        
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

        embed_message = discord.Embed(
            title=f'Documentos Fiscais',
            description='Selecione uma opção para buscar os documentos fiscais',
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )

        if isinstance(ctx_or_interaction, discord.Interaction):
            await ctx_or_interaction.response.send_message(embed=embed_message, view=view)
        else:
            await ctx_or_interaction.send(embed=embed_message, view=view)
    
    @commands.command(name='documentos', description='Busca documentos fiscais')
    async def documentos_prefix(self, ctx: commands.Context):
        await self.documentos_fiscais(ctx)
    
    @app_commands.command(name='documentos', description='Busca documentos fiscais')
    async def documentos_slash(self, interaction: discord.Interaction):
        await self.documentos_fiscais(interaction)

async def setup(bot):
    await bot.add_cog(Documentos(bot))