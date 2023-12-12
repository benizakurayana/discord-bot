from discord.ext import commands
import random

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

# Run the bot
bot.run('THE TOKEN')
