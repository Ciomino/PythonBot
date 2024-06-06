import discord
import random
from discord.ext import commands

# Configurazione degli intents per ottenere informazioni sui membri
intents = discord.Intents.default()
intents.members = True  

# Creazione dell'istanza del bot con il prefisso '!'
bot = commands.Bot(command_prefix='!', intents=intents)

# Evento che viene chiamato quando il bot è pronto
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Comando shuffle per spostare i membri da un canale vocale a uno o più canali vocali
@bot.command()
async def shuffle(ctx, from_channel: discord.VoiceChannel, *to_channels: discord.VoiceChannel):
    if not to_channels:
        await ctx.send("Devi specificare almeno un canale di destinazione.")
        return

    members = from_channel.members
    if not members:
        await ctx.send(f"Non ci sono membri nel canale vocale {from_channel.name}.")
        return

    random.shuffle(members)  # Mescola i membri in modo casuale

    # Calcola la distribuzione equa dei membri
    num_channels = len(to_channels)
    members_per_channel = len(members) // num_channels
    remainder = len(members) % num_channels

    # Distribuisci i membri nei canali
    start = 0
    for i, channel in enumerate(to_channels):
        end = start + members_per_channel + (1 if i < remainder else 0)
        members_to_move = members[start:end]
        start = end

        for member in members_to_move:
            try:
                await member.move_to(channel)
                await ctx.send(f"{member.display_name} è stato spostato in {channel.name}")
            except discord.Forbidden:
                await ctx.send(f"Non ho i permessi per spostare {member.display_name} in {channel.name}.")
            except discord.HTTPException as e:
                await ctx.send(f"Errore nello spostamento di {member.display_name}: {e}")



bot.run('TOKEN')
