from discord.ext import commands
import requests, os, discord, time


class LeagueCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.version = ''
        self.headers = {"X-Riot-Token": os.getenv("RIOT_API_KEY")}
    
    def setupData(self):
        url = 'https://ddragon.leagueoflegends.com/api/versions.json'
        response = requests.request("GET", url).json()
        if response[0] == self.version:
            return
        self.version = response[0]
        
        url = 'http://ddragon.leagueoflegends.com/cdn/12.11.1/data/en_US/champion.json'
        response = requests.request("GET", url).json()
        self.champIDs = self.champToId(response)
    
    def champToId(self, champJSON):
        d = {}
        for champ in champJSON['data']:
            champInfo = champJSON['data'][champ]
            key = champInfo['key']
            name = champInfo['id']
            d[key] = name
        return d

    def getCurrentGame(self, summoner):
        url = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
        summoner = 'Cahl'
        response = requests.request("GET", url + summoner, headers=self.headers).json()
        summonerId = response['id']
        url = 'https://na1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/'
        response = requests.request("GET", url + summonerId, headers=self.headers).json()
        return response
    
    def getMastery(self, summonerId, champId):
        url = f'https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonerId}/by-champion/{champId}'
        response = requests.request("GET", url, headers=self.headers).json()
        if 'championLevel' not in response:
            return 0
        return response['championLevel']
    
    def getRank(self, summonerId):
        url = f'https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerId}'
        response = requests.request("GET", url, headers=self.headers).json()
        d = {}
        for rank in response:
            if rank['queueType'] == "RANKED_FLEX_SR":
                d['flex'] = f'{rank["tier"]} {rank["rank"]}'
            elif rank['queueType'] == "RANKED_SOLO_5x5":
                d['solo'] = f'{rank["tier"]} {rank["rank"]}'

        return str(d)

    def toTuples(self, gameInfo):
        tups = []
        for i in range(len(gameInfo['names'])):
            tups.append((gameInfo['names'][i], gameInfo['champions'][i], gameInfo['masteries'][i]))
        return tups
    
    def generateEmbed(self, gameInfo):
        color = int("0xebc334", base=16)
        embed = discord.Embed(
            title="Live Game", color=color
        )
        tups = self.toTuples(gameInfo)
        for i in range(len(tups)):
            tups[i] = str(tups[i])
        team1 = tups[0:5]
        team2 = tups[5:]
        embed.add_field(name="Blue Team", value="\n".join(team1), inline=True)
        embed.add_field(name="Rank", value="\n".join(gameInfo['ranks'][0:5]), inline=True)
        embed.add_field(name="Red Team", value="\n".join(team2), inline=False)
        embed.add_field(name="Rank", value="\n".join(gameInfo['ranks'][5:]), inline=True)
        return embed

    @commands.command("gamestats")
    @commands.has_any_role("The Principal", "Bad Kid", "Admin", "DJ")
    async def gamestats(self, ctx):
        self.setupData()
        game = self.getCurrentGame('Cahl')

        if game['gameType'] != 'MATCHED_GAME':
            await ctx.send("This player is not in a game!")
            return

        gameInfo = {}
        players = game['participants']
        gameInfo['names'] = [user['summonerName'] for user in players]
        print(gameInfo['names'])
        gameInfo['champions'] = [self.champIDs[str(user['championId'])] for user in players]
        gameInfo['masteries'] = [self.getMastery(user['summonerId'], user['championId']) for user in players]
        time.sleep(2)
        gameInfo['ranks'] = [self.getRank(user['summonerId']) for user in players]

        embed = self.generateEmbed(gameInfo)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(LeagueCog(bot))
