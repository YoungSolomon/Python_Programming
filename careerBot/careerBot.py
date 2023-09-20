#Import api and ID libraries
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()

#Import discord bot library/verify bot token
import discord
from discord.ext import commands
import random
channel_ID = int(os.getenv("channel_ID"))
discordToken = os.getenv("discordToken")

#Import openai api/verify api token
import openai
openai.api_key = os.getenv("openapiToken")

#Assigns bot perms/command prefix
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=">", intents = intents)

#Terminal message on bot startup/channel notification
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('-------------------')
    channel = bot.get_channel(channel_ID)
    await channel.send("Hello, I am in the channel")

#Bot command to call openai api
@bot.command(name="chat")
async def chat(ctx, *, user_input):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are an quantitative finance professional giving career advice to a young college student at a mid tier public university who is trying to break into the field."},
            {"role": "user", "content": user_input}
            ],
            max_tokens = 1750,
    )

    chat_response = response.choices[0].message["content"]
    await ctx.send(chat_response)

#Gives bot the token so it can actually run
    #Redundant comment but I always forget this step so now I have to write it in...

bot.run(discordToken)
