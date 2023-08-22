import discord
from discord.ext import commands
import requests
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

cached_response = None

API_KEY = ""

@bot.command()
async def stats(ctx):
    await ctx.send("We will output stats here!!!")

@bot.command()
async def supply(ctx):
    api_url = "https://explorer.rethereum.org/api?module=stats&action=coinsupply"
    
    try:
        response = requests.get(api_url).json()
        await ctx.send(response)
    except Exception as e:
        error_message = f"Sorry we're unable to do that at this time."
        await ctx.send(error_message)

@bot.command()
async def blocknum(ctx):
    url = "https://explorer.rethereum.org/api?module=block&action=eth_block_number"

    try:
        response = requests.get(url).json()
        blocks = int(response.get("result"), 16)
        await ctx.send(blocks)
    except Exception as e:
        error_message = f"Sorry we're unable to do that at this time."
        await ctx.send(error_message)

@bot.command()
async def price(ctx):
    global cached_response
    if cached_response:
        await ctx.send(cached_response)
    else:
        await ctx.send("Response not available.")

async def request_and_cache():
    global cached_response
    url = "https://safe.trade/api/v2/peatio/public/markets/rthusdt/tickers"

    try:
        headers = {
            'User-Agent': 'RTH_DISCORD_BOT',
        }

        response = requests.get(url, headers=headers).json()
        cached_response  = response['ticker']['last']
        print("Updating price cache - " + cached_response)
        await asyncio.sleep(300)
    except Exception as e:
        print(str(e))
        await asyncio.sleep(300)
        
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    while True:
        await request_and_cache()

bot.run(API_KEY)