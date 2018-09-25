import discord
from discord.ext import commands
import humanify
import logging


class Info:
    # 
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def user(self, ctx, *, member: discord.Member):
        online = ''
        if str(member.status) == 'online':
            online = '✳️'
        elif str(member.status) == 'idle':
            online = '✳️'
        else:
            online = '🔴'
        info = discord.Embed(
            title='Informationen über "' + member.name + '"',
            color=member.colour,
            description='Beigetreten am "' + humanify.datetime(member.joined_at) + '"\n'
                        'Farben code: "' + str(member.colour) + '"\n'
                        'Status: ' + online + '\n'
                        'Erstellt am: "' + humanify.datetime(member.created_at) + '"\n'
                        '[User icon](' + member.avatar_url.replace('webp?size=1024', 'png') + ')'
        )
        info.set_author(name=member.name, icon_url=member.avatar_url.replace('webp?size=1024', 'png'))

        info.set_footer(
            text='Made by G3bE',
            icon_url='http://g3be.bplaced.net/Files/Pictures/finished.png'
        )

        await ctx.send(embed=info)

    @commands.command()
    async def server(self, ctx):
        guild = ctx.guild
        info = discord.Embed(
            title='Informationen über "' + guild.name + '"',
            color=0x206694,
            description='Erstellt am: "' + humanify.datetime(guild.created_at) + '"\n'
                        ''
                        '[Server icon](' + guild.icon_url.replace('webp?size=1024', 'png') + ')'
        )
        info.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        info.set_footer(
            text='Made by G3bE',
            icon_url='http://g3be.bplaced.net/Files/Pictures/finished.png'
        )
        await ctx.send(embed=info)

    @commands.command()
    async def help(self, ctx):
        PREFIX = self.bot.command_prefix
        embed = discord.Embed(
            title='Was ich kann, etc.',
            color=0x206694,
            description='Prefix=\'' + PREFIX + '\' \n'
                                               'Commands: \n' +
                        PREFIX + 'sleep - Bots müssen auch mal schlafen. \n' +
                        PREFIX + 'coinflip - Kopf oder Zahl? \n' +
                        PREFIX + 'uptime - Hilft niemandem wirklich. \n' +
                        PREFIX + 'gif - Alle lieben sie! Schreib was dahinter! \n' +
                        PREFIX + 'report {user mention} - meldet einen User. 3 Reports = mute! \n' +
                        PREFIX + 'server - Command für den Server. \n' +
                        PREFIX + 'user - Command für User. \n' +
                        PREFIX + 'urbdict {Suche} - Suche was im Urban-Dictonary. \n' +
                        PREFIX + 'wakeup {User} - Stupse jemanden an! \n' +
                        PREFIX + 'post {Post} - Lasse es andere liken! \n' +
                        PREFIX + 'posts - Schaue dir andere Posts an! \n' +
                        PREFIX + 'count {Anfang} {Ende} - Zu dumm zum zählen? \n' +
                        PREFIX + 'source {Command} - Schau in mich hinein. \n' +
                        PREFIX + 'say {tell} - Lass mich was sagen. \n' +
                        PREFIX + 'help - Dieser Command. \n \n'
                                 'Außerdem gibt es eine Join- und Leave-Message.'
        )
        embed.set_author(
            name='CaptianOverkill',
            icon_url='http://g3be.bplaced.net/Files/Pictures/CaptainOverkill.png'
        )

        embed.set_footer(
            text='Made by G3bE',
            icon_url='http://g3be.bplaced.net/Files/Pictures/finished.png'
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def source(self, ctx, *, ree):
        cogys = ['user', 'server', 'help', 'post', 'posts', 'uptime', 'report', 'sleep', 'coinflip', 'gif', 'urbdict', 'wakeup', 'count']
        if ree in cogys:
            await ctx.send('<a:youskid:493458639399419914>')
        elif ree == 'github':
            await ctx.send('Bitte nicht skidden: https://github.com/G3bE/CaptianOverkill/tree/commands-ext')
        else:
            await ctx.send('Für deine Eingabe "' + ree + '" gibt es leider keinen Eintrag!')

    # Error handling
    @user.error
    async def user_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.invoke(self.user, member=ctx.author)
            logging.info('Due to an missing argument the info command send info about the author!')

    @source.error
    async def source_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Benutzung: >source <command> - Beispiel >source gif')


def setup(bot: commands.bot):
    bot.add_cog(Info(bot=bot))
