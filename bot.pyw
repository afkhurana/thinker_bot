# <:thinking:263a7f4eeb6f69e46d969fa479188592>



# bot.py
import os
import discord
from dotenv import load_dotenv




load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_NAME = os.getenv('DISCORD_GUILD')
THOUGHTS_CHANNEL_NAME = os.getenv('THOUGHTS_CHANNEL')
VERBOSE = eval(os.getenv('VERBOSE'))



#initialize globals
glob_guild = None
glob_thoughts_channel = None


#initialize client
client = discord.Client()



@client.event
async def on_ready():
	#set glob_guild
	for guild in client.guilds:
		if guild.name == GUILD_NAME:
			glob_guild = guild
			print(f'{client.user} is thinking about guild {guild.name}')
			break 
	for channel in glob_guild.channels:
		if channel.name == THOUGHTS_CHANNEL_NAME:
			glob_thoughts_channel = channel
			print(f'{client.user} is thinking about channel {channel.name}')
			break


@client.event
async def on_message(message):
	if "all_messages" in VERBOSE:
		print(message.content)

	#reasons to not delete message
	if message.channel.name != THOUGHTS_CHANNEL_NAME:
		return
	if message.author == client.user:
		return
	if message.is_system():
		return

	if not (message.content.startswith("\U0001f914 thinking about") or message.content.startswith("\U0001f914thinking about")):
		print(f"Thinking about deleting @{message.author.name}'s message \"{message.content}\"")
		await message.delete()
	return


client.run(TOKEN)