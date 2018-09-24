import discord
from discord.ext import commands
import asyncio
import logging
import random
import requests, io, safygiphy


class Interact:
    def __init__(self, bot):
        self.bot = bot
        self.g = safygiphy.Giphy()

    @commands.command()
    async def sleep(self, ctx, *, sleep_time: float):
        if sleep_time > 5:
            await ctx.send('Zeit wurde auf 5 Sekunden gesetzt!')
            sleep_time = 5.0
            await asyncio.sleep(sleep_time)
        else:
            await asyncio.sleep(sleep_time)
        await ctx.send('Aufgewacht!')

    @commands.command()
    async def coinflip(self, ctx):
        choice = random.randint(1, 2)
        if choice == 1:
            await ctx.message.add_reaction('👨')
        elif choice == 2:
            await ctx.message.add_reaction('🎱')

    @commands.command()
    async def gif(self, ctx, *, query: str):
        rgif = self.g.random(tag=str(query))
        if self.bot.gifqueue >= 1:
            await ctx.send('Der Bot erhält momentan zu viele GIF Anfragen! Bitte warte ein bisschen!')
            return 1
        try:
            self.bot.gifqueue += 1
            response = requests.get(str(rgif.get("data", {}).get('image_original_url')), stream=True)
            await ctx.send(file=discord.File(io.BytesIO(response.raw.read()), 'video.gif'))
            self.bot.gifqueue -= 1
        except AttributeError:
            await ctx.send('Kein GIF gefunden... :´(')
            self.bot.gifqueue -= 1
        except Exception as e:
            error = discord.Embed(
                title='Error!',
                color=0xff0000,
                description=e.__str__()
            )
            await ctx.send(embed=error)

    @commands.command()
    async def urbdict(self, ctx, *, query: str):
        await ctx.send('https://www.urbandictionary.com/define.php?term=' + query.replace(' ', '+'))

    @commands.command()
    async def wakeup(self, ctx, user: discord.User):
        upwaker = discord.Embed(
            title='Hey, wake up!',
            color=0x206694,
            description=ctx.author.name + ' from ' + ctx.guild.name + ' wants you to wake up!'
        )
        await user.send(embed=upwaker)

    @commands.command()
    async def count(self, ctx, start, end):
        try:
            start = int(start)
            end = int(end)
        except ValueError:
            await ctx.send('Beide Argumente müssen Ganzzahlen sein!')
        if end > start:
            if (end - start) < 20:
                for i in range(start, end+1):
                    await ctx.send(i)
            else:
                await ctx.send('Soweit kann ich noch nicht zählen!')
        else:
            if (start - end) < 20:
                for i in range(start, end-1, -1):
                    await ctx.send(i)
            else:
                await ctx.send('Soweit kann ich noch nicht zählen!')

    # Error handling
    @sleep.error
    async def sleep_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.invoke(self.sleep, sleep_time=5.0)
            logging.info('Due to an missing argument the bot slept 5 seconds!')

    @gif.error
    async def gif_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Benutzung: >gif <query> - Beispiel >gif overkill')

    @urbdict.error
    async def urbdict_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Benutzung: >urbdict <query> - Beispiel >urbdict overkill')

    @wakeup.error
    async def wakeup_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Benutzung: >wakeup <user> - Beispiel >wakeup @G3bE6007')

    @count.error
    async def count_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Benutzung: >count <Anfang> <Ende> - Beispiel >count 4 10')


def setup(bot: commands.bot):
    bot.add_cog(Interact(bot=bot))
