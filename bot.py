import discord
from discord.ext import commands
from requests import get

TOKEN = "REDACTED"

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}')

@bot.tree.command(name="search-btc")
async def searchBtc(ctx: discord.Interaction, address: str):
    await ctx.response.defer()

    r = get(f"https://blockchain.info/rawaddr/{address}")
    data = r.json()
    
    if 'error' in data:
        embed = discord.Embed(
            title="<:Bitcoin:1337864688226140200> Wallet Not Found :x:",
            color=discord.Color.red()
        )
        embed.add_field(name="Error", value={data['error']})
    else:
        embed = discord.Embed(
            title="<:Bitcoin:1337864688226140200> Wallet Found",
            color=discord.Color.orange()
            )
        embed.add_field(name="Balance", value=f"**{data['final_balance'] / 100000000}** BTC")
        embed.add_field(name="Transactions", value=f"Total Received: **{data['total_received'] / 100000000}** BTC\nTotal Sent: **{data['total_sent'] / 100000000}** BTC\n[View Transactions](https://www.blockchain.com/explorer/addresses/btc/{address})")

    await ctx.followup.send(embed=embed)

@bot.tree.command(name="search-eth")
async def searchEth(ctx: discord.Interaction, address: str):
    await ctx.response.defer()

    r = get(f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey=EMPDNNDMX6GU6J9TCSGQQK74UK52VMDQ6Q")
    data = r.json()

    if data['message'] == "OK":
        embed = discord.Embed(
            title="<:Ethereum:1337864703304663100> Wallet Found",
            color=discord.Color(0x627feb)
            )
        embed.add_field(name="Balance", value=f"**{int(data['result']) / 10**18}** ETH\n")
        embed.add_field(name="Transactions", value=f"[View Transactions](https://etherscan.io/address/{address})")

    else:
        embed = discord.Embed(
            title="<:Ethereum:1337864703304663100> Wallet Not Found :x:",
            color=discord.Color.red()
        )
        embed.add_field(name="Error", value={data['result']})

    await ctx.followup.send(embed=embed)

@bot.tree.command(name="search-ltc")
async def searchLtc(ctx: discord.Interaction, address: str):
    await ctx.response.defer()

    r = get(f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance")
    data = r.json()

    if 'error' in data:
        embed = discord.Embed(
            title="<:Litecoin:1337871584266031185> Wallet Not Found :x:",
            color=discord.Color.red()
        )
        embed.add_field(name="Error", value={data['error']})
    else:
        embed = discord.Embed(
            title="<:Litecoin:1337871584266031185> Wallet Found",
            color=discord.Color(0x345d9d)
        )
        embed.add_field(name="Balance", value=f"**{int(data['balance']) / 100000000}** LTC\n")
        embed.add_field(name="Transactions", value=f"Total Received: **{int(data['total_received']) / 100000000}** LTC\nTotal Sent: **{int(data['total_sent']) / 100000000}** LTC\n[View Transactions](https://litecoinspace.org/address/{address})")

    await ctx.followup.send(embed=embed)

bot.run(TOKEN)
