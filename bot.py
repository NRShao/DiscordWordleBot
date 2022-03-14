import discord
from discord.ext import commands
import os, dotenv
from datetime import datetime
from pytz import timezone

dotenv.load_dotenv()

intents = discord.Intents(members=True, messages=True, reactions=True, guilds=True)
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

for filename in os.listdir("./cogs"):  # Change "cogs" to your folder name
    if filename.endswith(".py"):
        extension = f"cogs.{filename[:-3]}"
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")
    tz = timezone("EST")
    now = datetime.now(tz)
    await ctx.send(now)


@bot.command()
@commands.is_owner()
async def restart(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog = f"cogs.{filename[:-3]}"
            bot.reload_extension(cog)
    await ctx.send("Reloading...")


@bot.command()
async def help(ctx):
    color = int("0xebc334", base=16)
    embed = discord.Embed(
        title="Command List",
        description="How to use this bot!",
        color=color,
        timestamp=datetime.utcnow(),
    )
    wordle = "<#945166606613508176>"
    embed.add_field(
        name="Recording an answer",
        value="Copy paste your Wordle Copy Pasta into "
        + wordle
        + ". You can only answer the current days wordle based on EST.",
        inline=False,
    )
    embed.add_field(name="!stats", value="See your own answering stats.", inline=False)
    embed.add_field(name="!leaderboard", value="Check everyones rankings", inline=False)
    embed.add_field(
        name="!insult <tag user>", value="Check everyones rankings", inline=False
    )
    embed.add_field(name="!fb", value="Make fun of FB losses", inline=False)
    embed.add_field(name="!record", value="ME only", inline=False)
    embed.add_field(name="!answer", value="Deprecated", inline=True)

    await ctx.send(embed=embed)


bot.run(f"{os.getenv('ENV')}")
