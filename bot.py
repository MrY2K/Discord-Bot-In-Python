import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_NAME = os.getenv('DISCORD_GUILD')  # Make sure this is defined in your .env

# Set up intents and bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    # Start the background task for scheduled messages
    bot.loop.create_task(send_scheduled_message())

async def send_scheduled_message():
    await bot.wait_until_ready()
    
    # Find the general channel
    for guild in bot.guilds:
        if guild.name == GUILD_NAME:
            channel = discord.utils.get(guild.text_channels, name='general')
            if channel:
                break
    
    if not channel:
        print("General channel not found.")
        return
    
    while not bot.is_closed():
        now = datetime.now()
        target_time = datetime.combine(now.date(), datetime.strptime('00:54:00', '%H:%M:%S').time())
        
        # If it's already past the target time today, schedule for tomorrow
        if now > target_time:
            target_time += timedelta(days=1)
        
        # Calculate the time to wait
        wait_time = (target_time - now).total_seconds()
        print(f"Waiting for {wait_time} seconds until next scheduled message at {target_time}")
        
        await asyncio.sleep(wait_time)
        await channel.send("@everyone SESSION at 21:00, Don't Be Late")
        print(f"Message sent at {datetime.now()}")
        
        # Wait 24 hours before checking again
        await asyncio.sleep(24 * 60 * 60)

# Define the hello command
@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

# Run only the bot instance
bot.run(TOKEN)


# SIMPLE COMMAND WHEN THE USER TYPES !hello IT PRINTS The bot responds Hello!
# import os
# import discord
# from discord.ext import commands
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')

# # Set up intents and bot
# intents = discord.Intents.default()
# intents.message_content = True  # Required to read message content
# bot = commands.Bot(command_prefix='!', intents=intents)

# # Define the hello command
# @bot.command()
# async def hello(ctx):
#     await ctx.send('Hello!')

# # Run the bot
# bot.run(TOKEN)
