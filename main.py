import discord
from discord.ext import commands
import os
import random
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="-", intents=intents)
sad_words = ["sad", "teary", "disappointed","disheartened","sadge"]
ok_words = ["ok","fine",'alright']
# @bot.command()
#async def up(ctx, *, content: to_upper): can put funcitons into it as prerequisite
#    await ctx.send(content)


def choose_quote():
    with open("quotes.txt", "r") as file1:
        for i in range(random.randint(0,7)):
            file1.readline()
        return file1.readline()

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(name = "test")
async def ping(message, *, arg):
    await message.channel.send(arg)

@bot.command(name = "saysmth")
async def quote(message):
    await message.channel.send(choose_quote())

@bot.command(name = "add")
async def addition(message, *args: float):
    total = sum(args)
    await message.channel.send(f"the result is: {str(total)}")

@bot.command(name = "join")
async def on_joined(message,*, arg: discord.Member):
    await message.send(f"{arg} joined at {arg.joined_at}")

@bot.command(name = "shoot")
async def on_joined(message,*, arg: discord.Member):
    await message.send(f"{message.author} shooted {arg.global_name}! **Bang** they're dead! MWAHAHAHAHA")

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    if any(word in msg.content for word in sad_words):
        await msg.channel.send("are you ok?")
    elif any(word in msg.content for word in ok_words):
        await msg.channel.send("I am happy you think that!")

bot.run(os.getenv('TOKEN'))