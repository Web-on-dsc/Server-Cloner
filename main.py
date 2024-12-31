from os import system
import os
import psutil
import time
import sys
import discord
import asyncio
import colorama
from colorama import Fore, init
import platform
from dotenv import load_dotenv



load_dotenv()


token = os.getenv("token") # Faire un fichier nommé ".env" dans le même répertoire que le fichier et mettre son token sous ce format : token={tontoken}


if token is None:
    print("Erreur, token introuvable dans le .env")
    sys.exit(1)

class Clone:
    @staticmethod
    async def roles_delete(guild_to: discord.Guild):
            for role in guild_to.roles:
                try:
                    if role.name != "@everyone":
                        await role.delete()
                        print(f"Rôle {role.name} supprimé")
                except discord.Forbidden:
                    print(f"Erreur en supprimant le rôle {role.name}")
                except discord.HTTPException:
                    print(f"Impossible de supprimer le rôle {role.name}")

    @staticmethod
    async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
        roles = []
        role: discord.Role
        for role in guild_from.roles:
            if role.name != "@everyone":
                roles.append(role)
        roles = roles[::-1]
        for role in roles:
            try:
                await guild_to.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    colour=role.colour,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                print(f"Rôle {role.name} créé")
            except discord.Forbidden:
                print(f"Erreur en créant le rôle {role.name}")
            except discord.HTTPException:
                print(f"Impossible de créer le rôle {role.name}")

    @staticmethod
    async def channels_delete(guild_to: discord.Guild):
        for channel in guild_to.channels:
            try:
                await channel.delete()
                print(f"Salon {channel.name} supprimé")
            except discord.Forbidden:
                print(f"Erreur en supprimant le salon {channel.name}")
            except discord.HTTPException:
                print(f"Impossible de supprimer le salon {channel.name}")

    @staticmethod
    async def categories_create(guild_to: discord.Guild, guild_from: discord.Guild):
        channels = guild_from.categories
        channel: discord.CategoryChannel
        new_channel: discord.CategoryChannel
        for channel in channels:
            try:
                overwrites_to = {}
                for key, value in channel.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                new_channel = await guild_to.create_category(
                    name=channel.name,
                    overwrites=overwrites_to)
                await new_channel.edit(position=channel.position)
                print(f"Catégorie {channel.name} créée")
            except discord.Forbidden:
                print(f"Erreur en supprimant la catégorie {channel.name}")
            except discord.HTTPException:
                print(f"Impossible de supprimer la catégorie {channel.name}")

    @staticmethod
    async def channels_create(guild_to: discord.Guild, guild_from: discord.Guild):
        channel_text: discord.TextChannel
        channel_voice: discord.VoiceChannel
        category = None
        for channel_text in guild_from.text_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_text.category.name:
                            break
                    except AttributeError:
                        print(f"Le salon [texte] {channel_text.name} n'a pas de catégorie")
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_text.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position,
                        topic=channel_text.topic,
                        slowmode_delay=channel_text.slowmode_delay,
                        nsfw=channel_text.nsfw)
                except:
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print(f"Salon [texte] {channel_text.name} créé")
            except discord.Forbidden:
                print(f"Erreur en créant le salon [texte] {channel_text.name}")
            except discord.HTTPException:
                print(f"Impossible de créer le salon [texte] {channel_text.name}")
            except:
                print(f"Impossible de créer le salon [texte] {channel_text.name}")

        category = None
        for channel_voice in guild_from.voice_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_voice.category.name:
                            break
                    except AttributeError:
                        print(f"Le salon [vocal] {channel_voice.name} n'a pas de catégorie")
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_voice.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position,
                        bitrate=channel_voice.bitrate,
                        user_limit=channel_voice.user_limit,
                        )
                except:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print(f"Salon [vocal] {channel_voice.name} créé")
            except discord.Forbidden:
                print(f"Erreur en supprimant {channel_voice.name}")
            except discord.HTTPException:
                print(f"Impossible de créer salon [vocal] {channel_voice.name}")
            except:
                print(f"Impossible de créer salon [vocal] {channel_voice.name}")


    @staticmethod
    async def emojis_delete(guild_to: discord.Guild):
        for emoji in guild_to.emojis:
            try:
                await emoji.delete()
                print(f"Emoji {emoji.name} supprimé")
            except discord.Forbidden:
                print(f"Erreur en supprimant l'emoji {emoji.name}")
            except discord.HTTPException:
                print(f"Impossible de supprimer l'emoji {emoji.name}")

    @staticmethod
    async def emojis_create(guild_to: discord.Guild, guild_from: discord.Guild):
        emoji: discord.Emoji
        for emoji in guild_from.emojis:
            try:
                emoji_image = await emoji.url.read()
                await guild_to.create_custom_emoji(
                    name=emoji.name,
                    image=emoji_image)
                print(f"Emoji {emoji.name} créé")
            except discord.Forbidden:
                print(f"Erreur en créant l'emoji {emoji.name} ")
            except discord.HTTPException:
                print(f"Impossible de créer l'emoji {emoji.name}")

    @staticmethod
    async def guild_edit(guild_to: discord.Guild, guild_from: discord.Guild):
        try:
            try:
                icon_image = await guild_from.icon_url.read()
            except discord.errors.DiscordException:
                print(f"Impossible de lire l'image de {guild_from.name}")
                icon_image = None
            await guild_to.edit(name=f'{guild_from.name}')
            if icon_image is not None:
                try:
                    await guild_to.edit(icon=icon_image)
                    print(f"L'icône de {guild_to.name} à changé")
                except:
                    print(f"Erreur en changeant l'icône de {guild_to.name}")
        except discord.Forbidden:
            print(f"Impossible de changer l'icône de {guild_to.name}")


client = discord.Client()
os = platform.system()
if os == "Windows":
    system("cls")
else:
    system("clear")
    print(chr(27) + "[2J")
print(f"""{Fore.RED}
 
                                  ░██████╗███████╗██████╗░██╗░░░██╗███████╗██████╗░ ░█████╗░██╗░░░░░░█████╗░███╗░░██╗███████╗██████╗░
                                  ██╔════╝██╔════╝██╔══██╗██║░░░██║██╔════╝██╔══██╗ ██╔══██╗██║░░░░░██╔══██╗████╗░██║██╔════╝██╔══██╗
                                  ╚█████╗░█████╗░░██████╔╝╚██╗░██╔╝█████╗░░██████╔╝ ██║░░╚═╝██║░░░░░██║░░██║██╔██╗██║█████╗░░██████╔╝ by Web
                                  ░╚═══██╗██╔══╝░░██╔══██╗░╚████╔╝░██╔══╝░░██╔══██╗ ██║░░██╗██║░░░░░██║░░██║██║╚████║██╔══╝░░██╔══██╗
                                  ██████╔╝███████╗██║░░██║░░╚██╔╝░░███████╗██║░░██║ ╚█████╔╝███████╗╚█████╔╝██║░╚███║███████╗██║░░██║
                                  ╚═════╝░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝ ░╚════╝░╚══════╝░╚════╝░╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝
{Fore.RESET}""")
guild_s = input(f'[{Fore.RED}?{Fore.RESET}] Entre le serveur que tu veux copier:\n>')
guild = input(f'[{Fore.RED}?{Fore.RESET}] Entre le serveur où tu veux copier:\n >')
input_guild_id = guild_s  
output_guild_id = guild  



print("\n")

#by Web-on-dsc, que demander de plus ?
@client.event
async def on_ready():
    try:
        print(f"Connetcé en temps que : {client.user}")
        print("Clonage...")
        guild_from = client.get_guild(int(input_guild_id))
        guild_to = client.get_guild(int(output_guild_id))
        await Clone.guild_edit(guild_to, guild_from)
        await Clone.roles_delete(guild_to)
        await Clone.channels_delete(guild_to)
        await Clone.roles_create(guild_to, guild_from)
        await Clone.categories_create(guild_to, guild_from)
        await Clone.channels_create(guild_to, guild_from)
        print(f"""{Fore.GREEN}


                                                ░█████╗░██╗░░░░░░█████╗░███╗░░██╗███████╗██████╗░
                                                ██╔══██╗██║░░░░░██╔══██╗████╗░██║██╔════╝██╔══██╗
                                                ██║░░╚═╝██║░░░░░██║░░██║██╔██╗██║█████╗░░██║░░██║
                                                ██║░░██╗██║░░░░░██║░░██║██║╚████║██╔══╝░░██║░░██║
                                                ╚█████╔╝███████╗╚█████╔╝██║░╚███║███████╗██████╔╝
                                                ░╚════╝░╚══════╝░╚════╝░╚═╝░░╚══╝╚══════╝╚═════╝░

        {Fore.RESET}""")
        await asyncio.sleep(5)
        await client.close()
    except KeyboardInterrupt:
        os._exit(1)    


client.run(token, bot=False)
