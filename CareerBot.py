#import discord bot api
    #set a discord command to call the bot
    #assign the bot a login token and permissions
#import openai api
    #feed courseload to openai api
        #assign it as a professor 
#import google drive api
    #pull course links off google drive
#retrieve links from google drive


#Import discord.py (bot commands)
import discord
from discord.ext import commands
import random

#Import dotenv and os (api and token IDs)
import os
from dotenv import load_dotenv, dotenv_values


#Load dot env after import
load_dotenv()

#grabs our keys and apis from our env files to improve security and hide sensitive information such as apis and tokens
CHANNEL_ID = int(os.getenv('Channel_ID'))
TOKEN = os.getenv('Token')


#Assigning perms to discord bot, allows it to interact with members and messages by default
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

#Assigns the key to indicate a bot command as >, users who add this character before a message will call on the bot
bot = commands.Bot(command_prefix='>', intents = intents)

#Adds terminal log in message for the bot on startup, also grabs channel id and announces its presence to the channel
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('-----------')
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello, I am in the channel!")

#Command which takes user input and returns appropriate information as such
@bot.command()
async def Info(ctx, arg):
    if arg == "Intro":
        await ctx.send('I am a bot designed to assists one\`s future endeavors in a quantitative finance career! I have a myriad of useful references for the user to learn about and practice almost every facet of a career AND interviews. My materials include all your major components of required knowledge including but not limited to: Probability, Game Theory, Brain Teasers, Machine Learning, Algorithms and Data Structures, Interview Technique, Mental Math and even firm specific content such as Jane Street\'s interview guide and information on Optiver\`s infamous Zap N test. \n (try Command List for more options)')
    else:
        await ctx.send("I'm sorry, that is not a valid command")
        



#Gives our bot the token so it actually runs LMFAO
bot.run(TOKEN)

