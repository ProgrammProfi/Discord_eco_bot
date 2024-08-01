import discord
from discord.ext import commands
import difflib

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=discord.Intents.default())


with open("database.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    data = {}
    for i in lines:
        req = i.split("=")[0]
        ans = i.split("=")[1]
        data[req] = ans


def compare_strings(string1, string2):
    matcher = difflib.SequenceMatcher(None, string1, string2)
    return matcher.ratio() * 100


def max_match(name):
    max_pr = 0
    max_data_name = ""
    for i in data.keys():
        if compare_strings(i, name) > max_pr:
            max_pr = compare_strings(i, name)
            max_data_name = i
    if max_pr > 60:
        return max_data_name
    else:
        return None


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command("test")
async def test(ctx, name):
    if max_match(name) is None:
        await ctx.send("No data")
    else:
        await ctx.send(data[max_match(name)])

bot.run()
