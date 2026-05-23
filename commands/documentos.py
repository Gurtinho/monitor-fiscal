import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import io
import utils.log as log

from config import links
from utils import scrapper
from utils import download
from utils import ai_api
from utils import github_api
from utils import chunks

class Documentos(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    async def documentos_fiscais(self, ctx_or_interaction):

        # Função que roda quando o usuário seleciona uma opção
        async def select_callback(interaction: discord.Interaction):
            choice = interaction.data['values'][0]
            notas = scrapper.buscar_notas(choice)

            # Verificar e retornar o texto
            if isinstance(notas, str):
                await interaction.response.send_message(notas)
                return

            quantidade_notas = len(notas['documentos'])

            embed_message = discord.Embed(
                title=f'Documentos Fiscais - {choice}',
                description=f'Quantidade de documentos encontrados: {quantidade_notas}',
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow()
            )

            if notas['documentos']:
                for i in notas['documentos']:
                    embed_message.add_field(name=i['texto'], value=i['url'].replace(" ", ""), inline=False)
            else:
                embed_message.add_field(name='Aviso', value='Nenhum documento foi encontrado!', inline=False)
                embed_message.add_field(name='Status', value='Pode ficar suave e tomar seu café ☕', inline=False)

            # Configuração da view de resposta
            view_resultado = discord.ui.View()

            # Botão de download dos arquivos
            async def download_callback(btn_interaction: discord.Interaction):
                await btn_interaction.response.send_message("📦 Estou preparando o pacote com os documentos fiscais, aguarde...")
                file = await download.zipar(notas['documentos'], choice)
                await btn_interaction.followup.send(content="📦 Aqui está seu pacote zipado com os documentos fiscais:", file=file)
                await btn_interaction.delete_original_response()

            async def analisar_callback(btn_interaction: discord.Interaction):
                await btn_interaction.response.send_message("🔍 Estou analisando os documentos, aguarde...")
                arquivos = []
                for nota in notas['documentos']:
                    arquivo = await download.salvar_arquivo_local(nota['url'])
                    if arquivo:
                        arquivos.append(arquivo)
                try: 
                    if arquivos:
                        resultado = await ai_api.analisar(prompt_texto, arquivos)
                        blocos = chunks.dividir_texto(resultado)

                        await btn_interaction.delete_original_response()

                        for i, bloco in enumerate(blocos):
                            await btn_interaction.followup.send(content=bloco)
                            if i < len(blocos) - 1:
                                await asyncio.sleep(2)
                    else:
                        await btn_interaction.followup.send(content="Aconteceu alguma coisa e não consegui baixar e nem analisar seus arquivos 😥")
                except Exception as e:
                    await btn_interaction.followup.send(content=f"Aconteceu alguma coisa e não consegui baixar e nem analisar seus arquivos 😥 {e}")
                finally:
                    # Por fim remove os arquivos locais
                    for arquivo in arquivos:
                        await download.deletar_arquivo_local(arquivo)

            async def analisar_fontes_callback(btn_interaction: discord.Interaction):
                await btn_interaction.response.send_message("🔍 Estou analisando os documentos, aguarde...")
                arquivos = []
                for nota in notas['documentos']:
                    arquivo = await download.salvar_arquivo_local(nota['url'])
                    if arquivo:
                        arquivos.append(arquivo)

                
                # Baixa o código fonte do arquivo atual
                fonte = github_api.analisar_fontes(choice)
                arquivos.append(fonte)

                prompt_texto_fonte = prompt_texto + "\n\n Analise o código fonte do arquivo e me diga quais são as alterações que foram feitas."

                try: 
                    if arquivos:
                        resultado = await ai_api.analisar(prompt_texto, arquivos)
                        blocos = chunks.dividir_texto(resultado)

                        await btn_interaction.delete_original_response()

                        for i, bloco in enumerate(blocos):
                            await btn_interaction.followup.send(content=bloco)
                            if i < len(blocos) - 1:
                                await asyncio.sleep(2)
                    else:
                        await btn_interaction.followup.send(content="Aconteceu alguma coisa e não consegui baixar e nem analisar seus arquivos 😥")
                except Exception as e:
                    await btn_interaction.followup.send(content=f"Aconteceu alguma coisa e não consegui baixar e nem analisar seus arquivos 😥 {e}")
                finally:
                    # Por fim remove os arquivos locais
                    for arquivo in arquivos:
                        await download.deletar_arquivo_local(arquivo)

            # Botão de análise de arquivos
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

            # Botão de download dos arquivos
            btn_download = discord.ui.Button(label='Baixar Documentos', style=discord.ButtonStyle.success, emoji='📦')
            btn_download.callback = download_callback

            btn_analise = discord.ui.Button(label='Analisar Documentos', style=discord.ButtonStyle.blurple, emoji='🔍')
            btn_analise.callback = analisar_callback

            btn_analise_fontes = discord.ui.Button(label='Analisar Documentos e Fontes', style=discord.ButtonStyle.red, emoji='🔍')
            btn_analise_fontes.callback = analisar_fontes_callback
            
            # Botão de link
            btn_link = discord.ui.Button(label='Ir para Portal', style=discord.ButtonStyle.link, url=notas['url_portal'], emoji='🔗')

            # Gravar sequencia de botões
            view_resultado.add_item(btn_download)
            view_resultado.add_item(btn_analise)
            view_resultado.add_item(btn_analise_fontes)
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