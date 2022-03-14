from discord.ext import commands
import requests


class StocksCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("fb")
    @commands.has_any_role("The Principal", "Bad Kid", "Admin", "DJ")
    async def insult(self, ctx):
        url = "https://yfapi.net/v6/finance/quote"

        querystring = {"symbols": "FB"}

        headers = {"x-api-key": "Qkdfm9Y7nM8nxfbBay7JFae3qU7Kwjn95BrCoQ2x"}

        response = requests.request("GET", url, headers=headers, params=querystring)
        json = response.json()
        price = json["quoteResponse"]["result"][0]["regularMarketPrice"]
        day_percent_change = json["quoteResponse"]["result"][0][
            "regularMarketChangePercent"
        ]
        day_price_change = json["quoteResponse"]["result"][0]["regularMarketChange"]
        # sign = ''
        # if day_price_change < 0:
        #   day_price_change = abs(day_percent_change)
        #   sign = '-'
        await ctx.send(
            f"Today, Facebook stock is at **{price}** per share. It changed by **{round(day_percent_change, 2)}%** and **{round(day_price_change, 2)}** USD."
        )


def setup(bot):
    bot.add_cog(StocksCog(bot))
