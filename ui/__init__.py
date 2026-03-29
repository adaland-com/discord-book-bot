"""UI components for the book bot."""
import discord
from discord.ui import Button, View


class HelpButtons(View):
    """Interactive buttons for help menu"""
    
    def __init__(self):
        super().__init__(timeout=180)
    
    @discord.ui.button(label="Example: Title", style=discord.ButtonStyle.primary)
    async def title_example(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Type: `/book query: title: The Hobbit`", ephemeral=True)
    
    @discord.ui.button(label="Example: Author", style=discord.ButtonStyle.secondary)
    async def author_example(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Type: `/book query: author: Tolkien`", ephemeral=True)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger)
    async def close(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content="Help menu closed.", view=None, embed=None)
