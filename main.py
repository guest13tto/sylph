import discord
from discord.ext import tasks, commands
import os
import random
from datetime import datetime
import asyncio
import json
import requests
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG)
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="-", intents=intents, case_insensitive=True)
sad_words = ["sad", "teary", "disappointed","disheartened","sadge"]
ok_words = [" ok! ","fine",'alright']
day = str(int(datetime.now().strftime("%d")))
devel_server = ""
numsongs = 0
with open("database.json", "r") as f:
    data = json.load(f)

# @bot.command()
#async def up(ctx, *, content: to_upper): can put funcitons into it as prerequisite
#    await ctx.send(content)
async def send_message(file = None, content=None, msg = None, channel= None, guild = None,embeds = None):
    guild = guild if msg == None else msg.guild
    test = False
    if not test or guild is devel_server:
        if guild is devel_server:
            if embeds != None:
                if msg != None:
                    await msg.channel.send(file= file, embed=embeds)
                elif channel != None:
                    await channel.send(file= file,embed=embeds)
                else:
                    for channels in guild.text_channels:
                        await channels.send(file= file,embed=embeds)
            else:
                if msg != None:
                    await msg.channel.send(content)
                elif channel != None:
                    await channel.send(content)
                else:
                    for channels in guild.text_channels:
                        await channels.send(content)

            

def getGIF(searchTerm):
    response = requests.get("https://tenor.googleapis.com/v2/search?q=%s&key=%s&limit=1" %(searchTerm, os.getenv('TENORTOKEN')))
    ata = json.loads(response.content)  # `requests` doesn't need `json.loads()`
    return ata['results'][0]['media_formats']['gif']['url']

def choose_quote():
    with open("quotes.txt", "r") as file1:
        for i in range(random.randint(0,7)):
            file1.readline()
        return file1.readline()

@bot.event
async def on_ready():
    global devel_server
    print('We have logged in as {0.user}'.format(bot))
    devel_server = bot.get_guild(1241015660021288980)
    print(devel_server)

@bot.command(name = "q")
async def queue(msg):
    global numsongs
    queuelist = ""
    embedVar = discord.Embed(title="Page **1**/**5**", description="", color=0x42f581)
    embedVar.set_author(name="Sylph's Queue!")
    for i in range(1,6):
        embedVar.add_field(name = f"{i}. title - time", value="", inline=False)
    await send_message(embeds=embedVar, msg=msg)


@bot.command(name = "invite")
async def invite(msg):
    await send_message("https://discord.com/oauth2/authorize?client_id=1241008722839470141&permissions=1084533243456&scope=bot", msg = msg)
    
@bot.command(name = "test")
async def ping(message, *, arg):
    await send_message(arg, msg = message)
    # await message.channel.send(arg)

@bot.command(name = "saysmth")
async def quote(message):
    await send_message(choose_quote(), msg= message)

@bot.command(name = "add")
async def addition(message, *args: float):
    total = sum(args)
    await send_message(f"the result is: {str(total)}", msg=message)

@bot.command(name = "join")
async def on_joined(message,*, arg: discord.Member):
    await send_message(f"{arg} joined at {arg.joined_at}", msg=message)

@bot.command(name = "shoot")
async def blast(message,*, arg: discord.Member):
    await send_message(f"{message.author} shooted {arg.global_name}! **Bang** they're dead! MWAHAHAHAHA", msg=message)


@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    if any(word in msg.content for word in sad_words):
        await send_message("are you ok?", msg=msg)
    elif any(word in msg.content for word in ok_words):
        await send_message("I am happy you think that! ",msg=msg)
    await bot.process_commands(msg)


@bot.command(name = "gif")
async def find_gif(msg, *, args):
    await send_message(getGIF(args), msg=msg)



@tasks.loop(seconds = 30)
async def birthday():
    global day
    await bot.wait_until_ready()
    now = datetime.now()
    if now.strftime("%d") != day:
        for person in data["birthdays"]:
            if person["month"] == now.strftime("%B") and person["day"] == int(now.strftime("%d")):
                for guild in bot.guilds:
                    for channel in guild.text_channels:
                        if channel.position == 0:
                            name = person["name"]
                            url = getGIF("happy birthday anime girl")
                            await send_message(f"matthew is sleeping right now, but he really wants to wish you a happy birthday, so let me pass on this message from him: \n**{name}, HAPPY BIRTHDAY!!!**", channel)
                            await send_message(getGIF("happy birthday anime girl"),channel)
        day = now.strftime("%d")
                        



async def main():
    async with bot:
        birthday.start()
        await bot.start(os.getenv('TOKEN'))

asyncio.run(main())