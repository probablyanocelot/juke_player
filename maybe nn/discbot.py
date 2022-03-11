import os
import discord
import ctypes
import ctypes.util
from jukebot import get_bestquality
from search_yt import search_yt
from asgiref.sync import async_to_sync
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('.env')


GUILD = os.getenv('GUILD')
intents = discord.Intents.all()  # for channel(?) permissions
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='--')


@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(name='play', help='To play song')
async def play(ctx, terms):

    # https://stackoverflow.com/questions/63647546/how-would-i-stream-audio-from-pytube-to-ffmpeg-and-discord-py-without-downloadin
    # Solves a problem
    FFMPEG_OPTS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    # server = ctx.message.guild
    # voice_channel = server.voice_client
    channel = discord.utils.get(
        ctx.guild.voice_channels, name=ctx.message.author.voice.channel.name)
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if not voice is None:  # test if voice is None
        if not voice.is_connected():
            await channel.connect()
    else:
        await channel.connect()

    voice_channel = ctx.message.guild.voice_client

    # opus = ctypes.util.find_library('opus')

    # discord.opus.load_opus(opus)
    # if not discord.opus.is_loaded():
    #     raise RunTimeError('Opus failed to load')

    async with ctx.typing():
        url = await search_yt(terms)
        # .from_url(url, loop=bot.loop, stream=True)
        # filename = get_bestquality(url)
        # filename = await YTDLSource.from_url(url, loop=bot.loop)
        filename = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        voice_channel.play(discord.FFmpegPCMAudio(
            executable="/usr/local/lib/ffmpeg.exe", source=filename, **FFMPEG_OPTS), after=lambda e: print('done', e))
        voice_channel.is_playing()
    # await ctx.send('**Now playing:** {}'.format(filename))


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")


@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


# BOT
TOKEN = os.getenv('DISCORD_TOKEN')


bot.run(TOKEN)
