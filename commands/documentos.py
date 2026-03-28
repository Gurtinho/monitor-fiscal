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
                await interaction.response.send_message(notas, ephemeral=True)
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
                embed_message.add_field(name='Aviso', value='Nenhum documento encontrado!', inline=False)
                embed_message.add_field(name='Status', value='Pode ficar suave e tomar seu café ☕', inline=False)

            # Configuração da view de resposta
            view_resultado = discord.ui.View()

            # Botão de download dos arquivos
            async def download_callback(btn_interaction: discord.Interaction):
                await btn_interaction.response.send_message("📦 Estou preparando o pacotinho ZIP, aguarde...", ephemeral=True)
                file = await download.zipar(notas['documentos'], choice)
                await btn_interaction.followup.send(content="📦 Aqui está seu pacotinho ZIP:", file=file, ephemeral=True)
                await btn_interaction.delete_original_response()

            async def analisar_callback(btn_interaction: discord.Interaction):
                await btn_interaction.response.send_message("🔍 Estou analisando os documentos, aguarde...", ephemeral=True)
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
                            await btn_interaction.followup.send(content=bloco, ephemeral=True)
                            if i < len(blocos) - 1:
                                await asyncio.sleep(2)
                    else:
                        await btn_interaction.followup.send(content="Aconteceu alguma coisa e não consegui baixar e nem analisar seus arquivos 😥", ephemeral=True)
                except Exception as e:
                    await btn_interaction.followup.send(content=f"Aconteceu alguma coisa e não consegui baixar e nem analisar seus arquivos 😥 {e}", ephemeral=True)
                finally:
                    # Por fim remove os arquivos locais
                    for arquivo in arquivos:
                        await download.deletar_arquivo_local(arquivo)

            async def analisar_fontes_callback(btn_interaction: discord.Interaction):
                await btn_interaction.response.send_message("🔍 Estou analisando os documentos, aguarde...", ephemeral=True)
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
                            await btn_interaction.followup.send(content=bloco, ephemeral=True)
                            if i < len(blocos) - 1:
                                await asyncio.sleep(2)
                    else:
                        await btn_interaction.followup.send(content="Aconteceu alguma coisa e não consegui baixar e nem analisar seus arquivos 😥", ephemeral=True)
                except Exception as e:
                    await btn_interaction.followup.send(content=f"Aconteceu alguma coisa e não consegui baixar e nem analisar seus arquivos 😥 {e}", ephemeral=True)
                finally:
                    # Por fim remove os arquivos locais
                    for arquivo in arquivos:
                        await download.deletar_arquivo_local(arquivo)

            # Botão de análise de arquivos
            prompt_texto = """
                Você é um Analista Fiscal Sênior e Contador especializado em SPED, NF-e, CT-e e MDF-e.
                Sua missão é analisar o PDF da Nota Técnica (NT) fornecida e extrair as alterações de layout e regras de validação.
                Porém, sua resposta deve conter só o que for relevante, não responda oque você faz como etc, só responda com o que foi pedido.

                DIRETRIZES DE RESPOSTA:
                1. PÚBLICO-ALVO: Desenvolvedores de software. Use termos técnicos (tags, schema, boolean, string, etc).
                2. TOM DE VOZ: Direto, como um colega de trabalho avisando outro ("Olha, mudou isso aqui...").
                3. SEM ENROLAÇÃO: Ignore textos jurídicos ou introduções longas. Vá direto ao que impacta o XML.

                FORMATO DA RESPOSTA (SIGA RIGOROSAMENTE):

                # 📑 [Título da Alteração ou Campo Novo]
                **O que mudou:** [Breve explicação técnica do impacto na rotina do sistema]
                **Caminho no XML (XPath):** `[Ex: infNFe/det/prod/tagNova]`

                **Exemplo de Implementação:**
                '''xml
                [Insira aqui um trecho de exemplo do XML formatado com a alteração aplicada]
                '''

                **Regras de Rejeição (Se houver):**
                - [Código da Rejeição]: [Motivo resumido]

                ---
                (Use o separador --- entre cada alteração encontrada)

                REGRAS ADICIONAIS:
                - Se não houver alteração de layout (apenas prorrogação de prazo, por exemplo), responda apenas com um resumo curto.
                - Use obrigatoriamente as crases triplas (''') para blocos de código XML para que fiquem visíveis no Discord.
                - Mantenha a resposta total abaixo de 1800 caracteres para não quebrar o limite do chat.
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