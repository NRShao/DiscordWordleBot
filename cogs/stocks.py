from discord.ext import commands
import requests, os


class StocksCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("fb")
    @commands.has_any_role("The Principal", "Bad Kid", "Admin", "DJ")
    async def fb(self, ctx):
        await self.stock(ctx, "fb")

    @commands.command("stock")
    @commands.has_any_role("The Principal", "Bad Kid", "Admin", "DJ")
    async def stock(self, ctx, ticker):
        url = "https://yfapi.net/v6/finance/quote"

        querystring = {"symbols": ticker}

        headers = {"x-api-key": os.getenv("STOCKS")}

        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 403:
            await ctx.send(
                "This api likes to change its API keys. Likely broken. Ping fishy."
            )
            return
        json = response.json()
        if json["quoteResponse"]["result"] == []:
            await ctx.send("Invalid request, check your ticker")
            return
        name = json["quoteResponse"]["result"][0]["displayName"]
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
            f"Today, {name} ({ticker.upper()}) stock is at **{price}** per share. It changed by **{round(day_percent_change, 2)}%** and **{round(day_price_change, 2)}** USD."
        )


def setup(bot):
    bot.add_cog(StocksCog(bot))
