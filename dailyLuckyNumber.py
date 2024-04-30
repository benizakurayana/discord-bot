from discord.ext import commands
import random
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Reset token:
# https://discord.com/developers/applications/1050263697207066725/bot

# Get the bot token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Create a Bot instance with a command prefix
bot = commands.Bot(command_prefix='!')

# Dictionary to store the daily lucky numbers
daily_lucky_numbers = {}


@bot.event
async def on_ready():
    print('Bot is ready.')


@bot.command(name='lucky')
async def get_lucky_number(ctx):
    # Check if the user already has a lucky number for today
    if ctx.author.id in daily_lucky_numbers:
        lucky_number = daily_lucky_numbers[ctx.author.id]
    else:
        # Generate a new lucky number and store it for the user
        lucky_number = random.randint(1, 100)
        daily_lucky_numbers[ctx.author.id] = lucky_number

    await ctx.send(f'Your daily lucky number is: {lucky_number}')


@bot.command(name='clear')
async def clear_all_lucky_number(ctx):
    daily_lucky_numbers.clear()

# Run the bot
bot.run(BOT_TOKEN)
