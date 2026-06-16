import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import utils.log as log

from utils import download, ai_api, chunks
from utils import github_api
from services import repository

class Documentos(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    async def documentos_fiscais(self, ctx_or_interaction):

        async def select_callback(interaction: discord.Interaction):
            choice = interaction.data['values'][0]
            notas = await repository.buscar_documentos_formatados(choice)
            quantidade = len(notas['documentos'])

            embed = discord.Embed(
                title=f'Documentos Fiscais - {choice}',
                description=f'Quantidade de documentos encontrados: {quantidade}',
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow()
            )

            if notas['documentos']:
                for doc in notas['documentos']:
                    embed.add_field(name=doc['texto'], value=doc['url'].replace(" ", ""), inline=False)
            else:
                embed.add_field(name='Aviso', value='Nenhum documento encontrado ainda.', inline=False)
                embed.add_field(name='Status', value='Aguarde a próxima verificação automática ☕', inline=False)

            prompt_texto = """
                Atue como Especialista Fiscal de software (NF-e/CT-e/SPED). Extraia do PDF da NT apenas alterações de layout e validações.

                REGRAS:
                1. PROIBIDO: Saudações, introduções, conclusões, textos jurídicos ou explicações de contexto.
                2. Foque 100% no desenvolvedor. Seja telegráfico e extremamente conciso.
                3. Máximo de 1800 caracteres.

                FORMATO OBRIGATÓRIO (Use `---` entre alterações):
                # 📑 [Nome da Tag/Campo]
                **Impacto:** [Ação técnica exigida em 1 linha]
                **XPath:** `[Caminho]`
                ```xml
                [Trecho XML curto com a alteração]
                Rejeição: [Código] - [Motivo em 1 linha]
                Nota: Se a NT for apenas prorrogação de prazo, responda com uma única frase.
            """

            prompt_texto_fonte = prompt_texto + "\n\n Analise o código fonte do arquivo e me diga quais são as alterações que foram feitas."

            async def download_callback(btn: discord.Interaction):
                await btn.response.send_message("📦 Preparando o pacote, aguarde...")
                file = await download.zipar(notas['documentos'], choice)
                await btn.followup.send(content="📦 Aqui está seu pacote zipado:", file=file)
                await btn.delete_original_response()

            async def analisar_callback(btn: discord.Interaction):
                await btn.response.send_message("🔍 Analisando os documentos, aguarde...")
                arquivos = []
                for nota in notas['documentos']:
                    arquivo = await download.salvar_arquivo_local(nota['url'])
                    if arquivo:
                        arquivos.append(arquivo)
                try:
                    if arquivos:
                        resultado = await ai_api.analisar(prompt_texto, arquivos)
                        blocos = chunks.dividir_texto(resultado)
                        await btn.delete_original_response()
                        for i, bloco in enumerate(blocos):
                            await btn.followup.send(content=bloco)
                            if i < len(blocos) - 1:
                                await asyncio.sleep(2)
                    else:
                        await btn.followup.send(content="Não consegui baixar os arquivos 😥")
                except Exception as e:
                    log.logging.error(f"Erro ao analisar documentos: {e}")
                    await btn.followup.send(content=f"Erro ao analisar os arquivos 😥")
                finally:
                    for arquivo in arquivos:
                        await download.deletar_arquivo_local(arquivo)

            async def analisar_fontes_callback(btn: discord.Interaction):
                await btn.response.send_message("🔍 Analisando documentos e fontes, aguarde...")
                arquivos = []
                for nota in notas['documentos']:
                    arquivo = await download.salvar_arquivo_local(nota['url'])
                    if arquivo:
                        arquivos.append(arquivo)

                fonte = await asyncio.to_thread(github_api.analisar_fontes, choice)
                if fonte:
                    arquivos.append(fonte)

                try:
                    if arquivos:
                        resultado = await ai_api.analisar(prompt_texto_fonte, arquivos)
                        blocos = chunks.dividir_texto(resultado)
                        await btn.delete_original_response()
                        for i, bloco in enumerate(blocos):
                            await btn.followup.send(content=bloco)
                            if i < len(blocos) - 1:
                                await asyncio.sleep(2)
                    else:
                        await btn.followup.send(content="Não consegui baixar os arquivos 😥")
                except Exception as e:
                    log.logging.error(f"Erro ao analisar fontes: {e}")
                    await btn.followup.send(content=f"Erro ao analisar os arquivos 😥")
                finally:
                    for arquivo in arquivos:
                        await download.deletar_arquivo_local(arquivo)

            view_resultado = discord.ui.View()

            btn_download = discord.ui.Button(label='Baixar Documentos', style=discord.ButtonStyle.success, emoji='📦')
            btn_download.callback = download_callback

            btn_analise = discord.ui.Button(label='Analisar Documentos', style=discord.ButtonStyle.blurple, emoji='🔍')
            btn_analise.callback = analisar_callback

            btn_fontes = discord.ui.Button(label='Analisar com Fontes', style=discord.ButtonStyle.red, emoji='🔍')
            btn_fontes.callback = analisar_fontes_callback

            btn_link = discord.ui.Button(label='Ir para Portal', style=discord.ButtonStyle.link, url=notas['url_portal'], emoji='🔗')

            view_resultado.add_item(btn_download)
            view_resultado.add_item(btn_analise)
            view_resultado.add_item(btn_fontes)
            view_resultado.add_item(btn_link)

            await interaction.response.edit_message(embed=embed, view=view_resultado)

        selections = discord.ui.Select(placeholder='Selecione uma opção')
        selections.options = [
            discord.SelectOption(label='NFe', value='NFe'),
            discord.SelectOption(label='NFCe', value='NFCe'),
            discord.SelectOption(label='CTe', value='CTe'),
            discord.SelectOption(label='MDFe', value='MDFe'),
        ]
        selections.callback = select_callback

        view = discord.ui.View()
        view.add_item(selections)

        embed = discord.Embed(
            title='Documentos Fiscais',
            description='Selecione uma opção para buscar os documentos fiscais',
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )

        if isinstance(ctx_or_interaction, discord.Interaction):
            await ctx_or_interaction.response.send_message(embed=embed, view=view)
        else:
            await ctx_or_interaction.send(embed=embed, view=view)

    @commands.command(name='documentos', description='Busca documentos fiscais')
    async def documentos_prefix(self, ctx: commands.Context):
        await self.documentos_fiscais(ctx)

    @app_commands.command(name='documentos', description='Busca documentos fiscais')
    async def documentos_slash(self, interaction: discord.Interaction):
        await self.documentos_fiscais(interaction)

async def setup(bot):
    await bot.add_cog(Documentos(bot))
