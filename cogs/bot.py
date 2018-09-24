import discord
from discord.ext import commands
import humanify


class Bot:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def uptime(self, ctx):
        await ctx.send('Bot online since ' + humanify.datetime(self.bot.time))

    @commands.command()
    async def game(self, ctx):
        if ctx.author.id == self.bot.G3eID:
            game = ctx.message.content[6:]
            await self.bot.change_presence(activity=discord.Game(name=game))

    @commands.command(name="load")
    async def _load(self, ctx, *, cog: str):
        if ctx.author.id == self.bot.G3eID:
            if cog != "all":
                try:
                    self.bot.unload_extension('cogs.' + cog)
                    self.bot.load_extension('cogs.' + cog)
                except ImportError:
                    await ctx.send('The extension ' + cog + ' could not be imported. Maybe wrong path?')
                    return 1
                except discord.errors.ClientException:
                    await ctx.send('The extension ' + cog + ' must have a function setup!')
                    return 1
                except Exception as e:
                    await ctx.send('Unknown error occurred: ' + str(e))
                    return 1
            else:
                for cog in self.bot.cogs:
                    try:
                        self.bot.unload_extension('cogs.' + cog.lower())
                        self.bot.load_extension('cogs.' + cog.lower())
                    except ImportError:
                        await ctx.send('The extension ' + cog + ' could not be imported. Maybe wrong path?')
                        return 1
                    except discord.errors.ClientException:
                        await ctx.send('The extension ' + cog + ' must have a function setup!')
                        return 1
                    except Exception as e:
                        await ctx.send('Unknown error occurred: ' + str(e))
                        return 1

            await ctx.send('Success!')
        else:
            await ctx.send('Nur für den Owner verfügbar!')


def setup(bot: commands.bot):
    bot.add_cog(Bot(bot=bot))
