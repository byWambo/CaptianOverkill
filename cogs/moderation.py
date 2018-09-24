import discord
from discord.ext import commands
import extern


class Bot:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def report(self, ctx, *, ruser: discord.Member):
        trusted = discord.utils.find(lambda r: r.name == "trusted", ctx.author.roles)
        if extern.get_cooldown_end(user_id=ctx.author.id):
            if trusted is not None:
                firstReport = discord.utils.find(lambda r: r.name == "firstReport", ctx.guild.roles)
                secondReport = discord.utils.find(lambda r: r.name == "secondReport", ctx.guild.roles)
                thirdReport = discord.utils.find(lambda r: r.name == "thirdReport", ctx.guild.roles)
                muted = discord.utils.find(lambda r: r.name == "muted", ctx.guild.roles)
                report_count = 0
                for role in ruser.roles:
                    if role.name == 'thirdReport':
                        await ruser.add_roles(muted)
                        report_count = 4
                        break
                    elif role.name == 'secondReport':
                        report_count = 3
                        await ruser.add_roles(thirdReport)
                        break
                    elif role.name == 'firstReport':
                        report_count = 2
                        await ruser.add_roles(secondReport)
                        break
                    else:
                        report_count = 1
                        await ruser.add_roles(firstReport)
                if report_count == 4:
                    await ctx.send(ruser.name + ' wurde gemutet')
                    await ruser.send(
                        'Du wurdest auf ' + ctx.guild.name +
                        ' gemuted. Bitte schreibe einen \nModerator oder Administrator an um unmuted zu werden!')
                elif report_count == 3:
                    await ctx.send(ruser.name + ' wurde zum dritten Mal reportet')
                elif report_count == 2:
                    await ctx.send(ruser.name + ' wurde zum zweiten Mal reportet')
                elif report_count == 1:
                    await ctx.send(ruser.name + ' wurde zum ersten Mal reportet')
                extern.set_report_cd(ctx.author.id)
            else:
                await ctx.send('Du brauchst die "trusted"-Rolle um jemanden zu reporten!')
        else:
            await ctx.send('Warte eine Woche nachdem du einen User reportest hast!')

    @commands.command()
    async def setup(self, ctx):
        permissions = ctx.channel.permissions_for(ctx.author)
        if permissions.manage_guild is True:
            try:
                firstReport = discord.utils.find(lambda r: r.name == "firstReport", ctx.guild.roles)
                secondReport = discord.utils.find(lambda r: r.name == "secondReport", ctx.guild.roles)
                thirdReport = discord.utils.find(lambda r: r.name == "thirdReport", ctx.guild.roles)
                muted = discord.utils.find(lambda r: r.name == "muted", ctx.guild.roles)
                trusted = discord.utils.find(lambda r: r.name == "trusted", ctx.guild.roles)
                botcommands = discord.utils.find(lambda r: r.name == "bot-commands", ctx.guild.text_channels)

                await ctx.send('Starte setup..')

                if firstReport is None:
                    await ctx.guild.create_role(name='firstReport')
                if secondReport is None:
                    await ctx.guild.create_role(name='secondReport')
                if thirdReport is None:
                    await ctx.guild.create_role(name='thirdReport')
                if muted is None:
                    await ctx.guild.create_role(name='muted')
                if trusted is None:
                    await ctx.guild.create_role(name='trusted')
                if botcommands is None:
                    await ctx.guild.create_text_channel(name='bot-commands')
            except Exception as e:
                await ctx.send('Ich konnte NICHT alle Rollen und Channels erstellen! \n'
                               'Melde dich bei G3bE#6007 mit diesem Error\n' + str(e))
                return 1
            await ctx.send('Setup war erfolgreich!')
        else:
            await ctx.send('Diese Funktion ist nur für Member zugänglich die den Server managen dürfen!')

    @commands.command()
    async def patch(self, ctx, version:str, *, notes: str):
        if ctx.author.id == self.bot.G3eID:
            for i in self.bot.guilds:
                botchannel = discord.utils.find(lambda r: r.name == "bot-commands", i.channels)
                ePatch = discord.Embed(
                    title='Patch-Notes für Version ' + version,
                    color=0x206694,
                    description=notes)
                ePatch.set_author(
                    name='Notes by ' + ctx.author.name,
                    icon_url=ctx.author.avatar_url
                )

                ePatch.set_footer(
                    text='Made by G3bE',
                    icon_url='http://g3be.bplaced.net/Files/Pictures/finished.png'
                )
                if botchannel is not None:
                    await botchannel.send(embed=ePatch)
        # else:
        #    patchMan = discord.utils.find(lambda r: r.name == "patchMan", message.guild.roles)
        #    if patchMan in message.author.roles:
        #        set_server(message.guild.id)
        #    else:
        #        channel.send('Du bist nicht ¡PatchMAN¡')


def setup(bot: commands.bot):
    bot.add_cog(Bot(bot=bot))
