import discord
from discord.ext import commands
from discord import app_commands

from services import status_jira, status_github

CORES = {
    "none": discord.Color.green(),
    "minor": discord.Color.yellow(),
    "major": discord.Color.orange(),
    "critical": discord.Color.red(),
}

def _build_jira_embed(dados: dict) -> discord.Embed:
    embed = discord.Embed(
        title="Status — Jira / Atlassian",
        description=f"**{dados['description']}**",
        color=CORES.get(dados["indicator"], discord.Color.blurple()),
        timestamp=discord.utils.utcnow()
    )

    if dados["components"]:
        for comp in dados["components"]:
            emoji = "🟢" if comp["status"] == "operational" else "🔴"
            status_fmt = comp["status"].replace("_", " ").title()
            embed.add_field(name=comp["name"], value=f"{emoji} {status_fmt}", inline=True)
    else:
        embed.add_field(name="Componentes", value="Nenhum componente Jira encontrado", inline=False)

    embed.set_footer(text="atlassianstatus.com")
    return embed

def _build_github_embed(dados: dict) -> discord.Embed:
    embed = discord.Embed(
        title="Status — Github",
        description=f"**{dados['description']}**",
        color=CORES.get(dados["indicator"], discord.Color.blurple()),
        timestamp=discord.utils.utcnow()
    )

    if dados["components"]:
        for comp in dados["components"]:
            emoji = "🟢" if comp["status"] == "operational" else "🔴"
            status_fmt = comp["status"].replace("_", " ").title()
            embed.add_field(name=comp["name"], value=f"{emoji} {status_fmt}", inline=True)
    else:
        embed.add_field(name="Componentes", value="Nenhum componente Github encontrado", inline=False)

    embed.set_footer(text="githubstatus.com")
    return embed



class Status(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    async def status(self, ctx_or_interaction):

        async def select_callback(interaction: discord.Interaction):
            choice = interaction.data['values'][0]
            await interaction.response.defer()

            if choice == "jira":
                dados = await status_jira.checar_jira()
                if dados["erro"]:
                    await interaction.followup.send(f"⚠️ Não consegui verificar o status do Jira: {dados['erro']}")
                else:
                    await interaction.followup.send(embed=_build_jira_embed(dados))
            elif choice == "github":
                dados = await status_github.checar_github()
                if dados["erro"]:
                    await interaction.followup.send(f"⚠️ Não consegui verificar o status do Github: {dados['erro']}")
                else:
                    await interaction.followup.send(embed=_build_github_embed(dados))
            elif choice == "sefaz":
                # dados = await status_sefaz.checar_sefaz()
                # await interaction.followup.send(embed=_build_sefaz_embed(dados))
                await interaction.followup.send("Status da Sefaz ainda não implementado!")
            else:
                await interaction.followup.send("Ainda não implementado para essa opção!")

        selections = discord.ui.Select(placeholder='Selecione uma opção')
        selections.options = [
            discord.SelectOption(label='Jira', value='jira'),
            discord.SelectOption(label='Github', value='github'),
            discord.SelectOption(label='Sefaz', value='sefaz'),
        ]
        selections.callback = select_callback

        view = discord.ui.View()
        view.add_item(selections)

        embed = discord.Embed(
            title='Verificar Status',
            description='Selecione uma opção para verificar o status',
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )

        if isinstance(ctx_or_interaction, discord.Interaction):
            await ctx_or_interaction.response.send_message(embed=embed, view=view)
        else:
            await ctx_or_interaction.send(embed=embed, view=view)

    @commands.command(name='status', description='Verifica o status de algumas APIs')
    async def status_prefix(self, ctx: commands.Context):
        await self.status(ctx)

    @app_commands.command(name='status', description='Verifica o status de algumas APIs')
    async def status_slash(self, interaction: discord.Interaction):
        await self.status(interaction)

async def setup(bot):
    await bot.add_cog(Status(bot))
