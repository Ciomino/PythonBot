import discord
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True  # Assicurati di avere abilitato questo intent nel Developer Portal

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def shuffle(ctx, from_channel: discord.VoiceChannel, *to_channels: discord.VoiceChannel):
    if not to_channels:
        await ctx.send("Devi specificare almeno un canale di destinazione.")
        return

    members = from_channel.members
    random.shuffle(members)

    for member in members:
        target_channel = random.choice(to_channels)
        await member.move_to(target_channel)
        await ctx.send(f"{member.display_name} è stato spostato in {target_channel.name}")

bot.run('token')
