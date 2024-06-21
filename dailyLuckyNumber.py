from discord.ext import commands
from dotenv import load_dotenv
import random
import os
from datetime import datetime


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


@bot.command(name='coin')
async def flip_a_coin(ctx):
    result = random.choice('*HEAD*', '*TAIL')
    await ctx.send(f'It\'s {result}!')


@bot.command(name='choose')
async def choose(ctx, *, options):
    # Split the options by commas and strip whitespace from each option
    option_list = [option.strip() for option in options.split(",")]

    if len(option_list) < 2:
        await ctx.send("Please provide at least two options.")
        return

    options_str = ', '.join(option_list)

    # Randomly choose among the provided options
    chosen_option = random.choice(option_list)
    # Send the result to the channel
    await ctx.send(f"Options are: {options_str}")
    await ctx.send(f"🎲 I choose: {chosen_option}")


# Dictionary to store sign-in times
signin_times = {}


@bot.command(name='signin')
async def signin(ctx, *, task_name):
    user_id = ctx.author.id
    task_name_str = ''.join(task_name)
    current_time = datetime.now()
    signin_times[(user_id, task_name_str )] = current_time
    current_time_format = current_time.strftime('%Y-%m-%d %H:%M:%S')
    await ctx.send(f'{ctx.author.mention} signed in for task "{task_name_str}" at {current_time_format} ({current_time})')


@bot.command(name='signout')
async def signout(ctx, *, task_name):
    user_id = ctx.author.id
    task_name_str = ''.join(task_name)
    current_time = datetime.now()
    if (user_id, task_name_str) in signin_times:
        signin_time = signin_times.pop((user_id, task_name_str))
        time_diff = current_time - signin_time
        days = time_diff.days
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Construct the time spent string
        time_spent = []
        if days > 0:
            time_spent.append(f"{days} days")
        if hours > 0 or days > 0:  # Include hours if there are any days
            time_spent.append(f"{hours} hours")
        if minutes > 0 or hours > 0 or days > 0:  # Include minutes if there are any days or hours
            time_spent.append(f"{minutes} minutes")
        time_spent.append(f"{seconds} seconds")
        current_time_format = current_time.strftime('%Y-%m-%d %H:%M:%S')
        await ctx.send(f'{ctx.author.mention} signed out from task "{task_name_str}" at {current_time_format} ({current_time}). Time spent: {" ".join(time_spent)}')
    else:
        await ctx.send(f'{ctx.author.mention}, you have not signed in for task "{task_name_str}".')


# Run the bot
bot.run(BOT_TOKEN)
