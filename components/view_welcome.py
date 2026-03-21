import discord

class ViewWelcome(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.success, custom_id="persistent_view:verify")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(self.channel)
        await interaction.user.add_roles(role)
        await interaction.response.send_message("You have been verified!", ephemeral=True)