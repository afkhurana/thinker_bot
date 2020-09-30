# <:thinking:263a7f4eeb6f69e46d969fa479188592>



# bot.py
import os
import discord
from dotenv import load_dotenv




load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_NAME = os.getenv('DISCORD_GUILD')
THOUGHTS_CHANNEL_NAME = os.getenv('THOUGHTS_CHANNEL')
ACCEPT_THONK = ( os.getenv('ACCEPT_THONK') == "True" )
VERBOSE = eval(os.getenv('VERBOSE'))



#initialize globals
glob_guild = None
glob_thoughts_channel = None
glob_thonk_emoji = None

#initialize client
client = discord.Client()



@client.event
async def on_ready():
	#set glob_guild
	for guild in client.guilds:
		if guild.name == GUILD_NAME:
			global glob_guild
			glob_guild = guild
			print(f'{client.user} is thinking about guild {guild.name}')
			break 
	for channel in glob_guild.channels:
		if channel.name == THOUGHTS_CHANNEL_NAME:
			global glob_thoughts_channel
			glob_thoughts_channel = channel
			print(f'{client.user} is thinking about channel {channel.name}')
			break

	for emoji in client.emojis:
		if emoji.name == "thonk":
			global glob_thonk_emoji
			glob_thonk_emoji = emoji
			print(f"Found thonk emoji {glob_thonk_emoji}"
					f"\n\twith ID {glob_thonk_emoji.id}")
			break
	return


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

	if ACCEPT_THONK:
		acceptable_message = (message.content.startswith("\U0001f914 thinking about")
				or message.content.startswith("\U0001f914thinking about") 
				or message.content.startswith("<:thonk:" + str(glob_thonk_emoji.id)
					+ "> thinking about")
				or message.content.startswith("<:thonk:" + str(glob_thonk_emoji.id)
					+ ">thinking about") )
	else:
		acceptable_message = (message.content.startswith("\U0001f914 "
													"thinking about")
				or message.content.startswith("\U0001f914thinking about") )
	if not acceptable_message:
		if message.content.startswith("thinking about"):
			new_message = "\U0001f914 " + message.content
			print(f"Thinking about changing @{message.author.name}"
					f"'s message \"{message.content}\" to "
					f"{new_message}")
			await message.delete()
			await message.channel.send(content=f"What @{message.author} "
												"meant to say was: "
												f"{new_message}")
		else:
			print(f"Thinking about deleting @{message.author.name}"
					f"'s message \"{message.content}\"")
			await message.delete()
	return


client.run(TOKEN)