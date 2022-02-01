import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
from discord.ext import commands,tasks
from pytube import YouTube
from pytube import Search
import pafy
import asyncio
from discord import FFmpegPCMAudio


bot = commands.Bot(command_prefix = '//')

check = False

@bot.command(name = "hello")
async def hello(ctx):
  await ctx.send("Hello {}".format(ctx.author))

@bot.command(name = "kill")
async def kill(ctx, args):
  await ctx.send("{} has beeen eliminated".format(args))

@bot.command(name = "speechless")
async def speechless(ctx):
  await ctx.send(file=discord.File('speechless.gif'))

@bot.command(name = "UPcm")
async def upcm(ctx):
  await ctx.send(file=discord.File('upcm.jpg'))

@bot.command(name = "play" ,aliases=["p"])
async def play(ctx, *args):

  global check
  
  global s
  voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

  if voice == None:
    if not ctx.message.author.voice:
      await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
      return
    else:
      channel = ctx.message.author.voice.channel
      await channel.connect()
    
  server = ctx.message.guild
  vc = server.voice_client
  


  
  if not check:
    check = not check
    s = Search(' '.join(args))
    j = 1
    output = "**Please select a track with the** `//play 1-5` **command:**\n"
    for i in s.results:
      title = (i.title).encode('utf8')
      output += '**' + str(j) + ': **'
      output += (title.decode('utf8')) + '\n'
      if j == 5:
        break
      j += 1
    
    global message
    message = await ctx.send(output)



  else:
    if not args[0].isnumeric():
      await ctx.send("Choose index number of song.")
      return

    check = not check
    if vc.is_playing():
      vc.stop()
    vdo_index = eval(args[0])
    vdo_id = s.results[vdo_index-1].video_id

    p = pafy.new(vdo_id)
    ba = p.getbestaudio()



    try :


      async with ctx.typing():
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        
        vc.play(FFmpegPCMAudio(ba.url, **FFMPEG_OPTIONS))
        vc.is_playing()

        await message.edit(content ='**Now playing:** {}'.format(p.title))
    except:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Paused. Use resume command to resume.")

    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()
        await ctx.send("Resumed")

    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Stopped")
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@bot.command(name = 'guessmybday', help = "Guesses your birthday")
async def guessmybday(ctx):
  count = 0
  msg = await ctx.send("**Is your birthday in the following set?**\n 1  3   5   7\n 9  11  13  15\n17  19  21  23\n25  27  29 31\n")

  check = lambda m: m.author == ctx.author and m.channel == ctx.channel

  try:
    confirm = await bot.wait_for("message", check=check, timeout=60)
  except asyncio.TimeoutError:
    await msg.edit(content="Guessing cancelled, timed out.")
    return

  if confirm.content == "yes" or confirm.content == "no":
    if confirm.content == "yes":
      count += 1
    await msg.edit(content = "**Is your birthday in the following set?**\n 2   3   6   7\n10  11  14  15\n18  19 22  23\n26  27  30  31\n")
    
  
  check = lambda m: m.author == ctx.author and m.channel == ctx.channel

  try:
    confirm = await bot.wait_for("message", check=check, timeout=60)
  except asyncio.TimeoutError:
    await msg.edit(content="Guessing cancelled, timed out.")
    return
  
  if confirm.content == "yes" or confirm.content == "no":
    if confirm.content == "yes":
      count += 2
    await msg.edit(content = "**Is your birthday in the following set?**\n 4   5   6   7\n12  13  14  15\n20  21  22  23\n28  29  30  31\n")
  
  check = lambda m: m.author == ctx.author and m.channel == ctx.channel

  try:
    confirm = await bot.wait_for("message", check=check, timeout=60)
  except asyncio.TimeoutError:
    await msg.edit(content="Guessing cancelled, timed out.")
    return
  
  if confirm.content == "yes" or confirm.content == "no":
    if confirm.content == "yes":
      count += 4
    await msg.edit(content = "**Is your birthday in the following set?**\n 8  9  10  11\n12  13  14  15\n24  25  26  27\n28  29 30  31\n")
  
  check = lambda m: m.author == ctx.author and m.channel == ctx.channel

  try:
    confirm = await bot.wait_for("message", check=check, timeout=60)
  except asyncio.TimeoutError:
    await msg.edit(content="Guessing cancelled, timed out.")
    return
  
  if confirm.content == "yes" or confirm.content == "no":
    if confirm.content == "yes":
      count += 8
    await msg.edit(content = "**Is your birthday in the following set?**\n16  17  18  19\n20  21  22  23\n24  25  26  27\n28  29  30  31\n")

  check = lambda m: m.author == ctx.author and m.channel == ctx.channel

  try:
    confirm = await bot.wait_for("message", check=check, timeout=60)
  except asyncio.TimeoutError:
    await msg.edit(content="Guessing cancelled, timed out.")
    return

  if confirm.content == "yes" or confirm.content == "no":
    if confirm.content == "yes":
      count += 16
    await msg.edit(content = "Your Birthday is on **" + str(count) + "**")
  return






keep_alive() 
bot.run(os.getenv('TOKEN'))