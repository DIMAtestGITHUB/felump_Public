from Key import key_ds
import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())

import discord
from discord.ext import commands
import yt_dlp

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Бот запущен как {bot.user}')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()

#@bot.command()
#async def play(ctx, url):
#    if not ctx.voice_client:
#        await ctx.author.voice.channel.connect()#

    #ydl_opts = {'format': 'bestaudio'}
    #with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #    info = ydl.extract_info(url, download=False)
    #    url2 = info['url']
    #    title = info['title']

    #source = await discord.FFmpegOpusAudio.from_probe(url2)
    #ctx.voice_client.play(source)

    #await ctx.send(f"Играет: {title}")

FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"

YDL_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

@bot.command()
async def play(ctx, url: str):
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.send("Сначала зайди в голосовой канал.")
        return

    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()

    try:
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)

            if "entries" in info:
                info = info["entries"][0]

            stream_url = info["url"]
            title = info.get("title", "Без названия")

        source = discord.FFmpegPCMAudio(
            stream_url,
            executable=FFMPEG_PATH,
            **FFMPEG_OPTIONS
        )

        ctx.voice_client.stop()
        ctx.voice_client.play(source)

        await ctx.send(f"Сейчас играет: {title}")

    except Exception as e:
        await ctx.send(f"Ошибка: {e}")


bot.run(key_ds)
