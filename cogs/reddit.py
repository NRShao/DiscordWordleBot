from discord.ext import commands
import requests, os


class RedditCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def request_token(self):
        client = os.getenv("REDDIT_CLIENT_ID")
        secret = os.getenv("REDDIT_SECRET")
        username = os.getenv("REDDIT_USERNAME")
        password = os.getenv("REDDIT_PASSWORD")
        client_auth = requests.auth.HTTPBasicAuth(client, secret)
        post_data = {
            "grant_type": "password",
            "username": username,
            "password": password,
        }
        headers = {"User-Agent": "LNLBot/0.1 by LNLDiscordBot"}
        response = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=client_auth,
            data=post_data,
            headers=headers,
        )
        json = response.json()
        return json["access_token"]

    def get_top_pasta(self, token):
        headers = {"User-Agent": "LNLBot/0.1 by LNLDiscordBot"}
        headers = {**headers, **{"Authorization": f"bearer {token}"}}
        response = requests.get(
            "https://oauth.reddit.com/r/copypasta/top.json?limit=1&t=day",
            headers=headers,
        )
        json = response.json()
        pasta = json["data"]["children"][0]["data"]["selftext"]
        return pasta.strip(" \n")

    @commands.command("copypasta")
    @commands.has_any_role("The Principal", "Bad Kid", "Admin", "DJ")
    async def copypasta(self, ctx):
        token = self.request_token()
        pasta = self.get_top_pasta(token)
        await ctx.send(f"Todays top copypasta: \n\n{pasta}")


def setup(bot):
    bot.add_cog(RedditCog(bot))
