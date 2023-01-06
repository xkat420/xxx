import os
import random

import discord
import asyncio
from datetime import datetime
from discord import app_commands
from googletrans import Translator
from spinhandlerselenium import spin_text
from spinhandlerseleniumv2 import spin_text as spin_text_v2

# SCOPE = https://discord.com/api/oauth2/authorize?client_id=1060269212301533394&permissions=11328&scope=bot

guildid = 639822603728453632

images_path = "/home/goupil/Documents/DiscordRobotImages/"

translator = Translator()


def get_random_img(): 
    return discord.File(
        f"{images_path}{random.choice(os.listdir(images_path))}",
        filename="consciousness.png"
    )


def translate_fr_en(lang, data):
    translated = translator.translate(text=data, dest='en').text
    print("+\n\n" + translated)
    spinned, xs = spin_text(lang, translated)
    xs.quit()
    retranslate = translator.translate(text=spinned, dest='fr').text
    print("+\n\n" + retranslate)
    return retranslate


def translate_fr_en_v2(lang, data):
    translated = translator.translate(text=data, dest='en').text
    print("+\n\n" + translated)
    spinned, xs = spin_text_v2(lang, translated)
    xs.quit()
    retranslate = translator.translate(text=spinned, dest='fr').text
    print("+\n\n" + retranslate)
    return retranslate

class Aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=guildid))
            self.synced = True
        print("Cancer")


client = Aclient()
tree = app_commands.CommandTree(client)


@tree.command(name="spin", description="Je refais ta paragraphe en mieux !", guild=discord.Object(id=guildid))
async def spin_command(interaction: discord.Interaction, paragraphe: str):
    await interaction.response.defer()
    
    spinned_text = translate_fr_en("English", paragraphe)

    embed = create_embed(paragraphe, spinned_text, interaction.user)
    xs = await interaction.followup.send(embed=embed)

    await xs.add_reaction("✅")
    await xs.add_reaction("❌")
    await xs.add_reaction("🔄")







async def temp_workingedit(msg, x1, user):
    firstcut = x1.split("**Nouvelle version**")
    secondcut = firstcut[0].split("""**Texte d'origine**
> """)

    embed = create_embed(
        secondcut,
        "Je prévois d'écrire un nouveau paragraphe en fonction du contexte que vous m'avez fournis ⏳ ..\nAttendez quelques petites secondes, s'il vous plaît 🤖 👽",
        user
    )

    firstcut = x1.split("**Nouvelle version**")
    secondcut = firstcut[0].split("""**Texte d'origine**
> """)

    spinned_text = translate_fr_en("English", secondcut)
    embed = create_embed(secondcut, spinned_text, user)
    await msg.edit(embed=embed)
    await msg.clear_reactions()
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")
    await msg.add_reaction("🔄")
    await msg.edit(embed=embed)










async def on_raw_reaction_add(payload):
    user = await client.fetch_user(payload.user_id)
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    emoji = str(payload.emoji)

    # Return if the user reacting is a bot
    if user.bot:
        return

    # Check if the user reacting is the original message author or the bot owner
    if payload.member.name != message.embeds[0].author.name and payload.member.id != 1054681455307018251:
        print("Access denied")
        await message.remove_reaction(payload.emoji, user)
        return

    if emoji == "🔙" and "🔙" == message.reactions[0].emoji:
        await message.clear_reactions()
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        await message.add_reaction("🔄")
        return

    if emoji == "⭐" and "⭐" == message.reactions[-1].emoji:
        return

    # Remove reaction if it is not a valid reaction
    if emoji != "✅" and emoji != "❌" and emoji != "🔄":
        await message.remove_reaction(emoji, user)
        return

    if emoji == "❌":
        await message.delete()
        return

    if emoji == "✅":
        await message.clear_reactions()
        await message.add_reaction("🔙")
        await message.add_reaction("⭐")
        return

    if emoji == "🔄" and user.id != client.user.id:
        await message.clear_reactions()
        await message.add_reaction("📝")
        await message.add_reaction("⏳")
        origintext = message.embeds[0].description
        await temp_workingedit(message, origintext, user)
        return

    if emoji == "⭐":
        await message.add_reaction("⭐")
        await message.add_reaction("🔙")
        await message.remove_reaction("✅", client.user)
        await message.remove_reaction("❌", client.user)
        await message.remove_reaction("🔄", client.user)
        return









def create_embed(original_text: str, new_text: str, user: discord.User):
    """Create and return an Embed object for the spin command."""
    embed = discord.Embed(
        title="✍️ ・ Skritur",
        description=
        "*Améliorez votre plume, avec l'intelligence artificielle !*\n\n**Texte d'origine**\n> " +
        original_text +
        "\n\n**Nouvelle version**\n> " +
        new_text +
        "\n\n**Skritur as-t-il fait un bon boulot ? Votre avis l'aide a s'améliorer**\nSi le rendu vous deplai, cliquez sur ``🔄 Relancer``\n──・─__─────__─__────__─__───__─__──__────────────"
    )
    embed.set_footer(text="Hollved ・ Skritur", icon_url="https://cdn.discordapp.com/attachments/1045358677089062963/1060899624489078794/Fichier_7.png")
    embed.set_author(name=user.name, icon_url=user.display_avatar)
    embed.set_image(url="https://cdn.discordapp.com/attachments/1045358677089062963/1060589734331699321/Ligne_invisible_hollved.png")
    return embed



client.run('MTA2MDI2OTIxMjMwMTUzMzM5NA.GdayJ5.Ryp_A2pVeJPjLYDIztlG7LVyi7HAV6d_gp9i50')