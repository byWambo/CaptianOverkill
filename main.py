import discord
from discord.ext import commands
import logging
import time, datetime
import secrets

logging.basicConfig(level=logging.INFO)

TOKEN = secrets.TOKEN

bot = commands.Bot(command_prefix=secrets.PREFIX)
bot.remove_command('help')

bot.G3eID = secrets.MyID
bot.gifqueue = 0
bot.posts = []

cogs = [
    'cogs.interact',
    'cogs.info',
    'cogs.bot',
    'cogs.moderation',
    'cogs.instacord'
]

for cog in cogs:
    bot.load_extension(cog)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    bot.time = datetime.datetime.now()

    await bot.change_presence(activity=discord.Game(name='Booting...'))
    time.sleep(2)
    act = discord.Activity(application_id=491218014142857219, name='dich', type=discord.ActivityType(2))
    await bot.change_presence(activity=act)


@bot.event
async def on_member_join(member):
    serverchannel = discord.utils.find(lambda r: r.name == "bot-commands", member.guild.channels)
    msg = "{0} ist {1} beigetreten!".format(member.mention, member.guild.name)
    await serverchannel.send(content=msg)


@bot.event
async def on_member_remove(member):
    serverchannel = discord.utils.find(lambda r: r.name == "bot-commands", member.guild.channels)
    msg = "{0} hat {1} tragischer Weise verlassen!".format(member.mention, member.guild.name)
    await serverchannel.send(content=msg)


@bot.event
async def on_guild_join(guild):
    serverchannel = discord.utils.find(lambda r: r.name == "willkommen", guild.channels)
    await serverchannel.send(content='Hey there! \nI am Captain Overkill with a B. \n'
                                     'Ich werde nur schnell ein paar Rollen und Channels erstellen!')
    try:
        firstReport = discord.utils.find(lambda r: r.name == "firstReport", guild.roles)
        secondReport = discord.utils.find(lambda r: r.name == "secondReport", guild.roles)
        thirdReport = discord.utils.find(lambda r: r.name == "thirdReport", guild.roles)
        muted = discord.utils.find(lambda r: r.name == "muted", guild.roles)
        trusted = discord.utils.find(lambda r: r.name == "trusted", guild.roles)
        botcommands = discord.utils.find(lambda r: r.name == "bot-commands", guild.text_channels)

        await serverchannel.send('Starte setup..')

        if firstReport is None:
            await guild.create_role(name='firstReport')
        if secondReport is None:
            await guild.create_role(name='secondReport')
        if thirdReport is None:
            await guild.create_role(name='thirdReport')
        if muted is None:
            await guild.create_role(name='muted')
        if trusted is None:
            await guild.create_role(name='trusted')
        if botcommands is None:
            await guild.create_text_channel(name='bot-commands')
    except Exception as e:
        await serverchannel.send('Ich konnte NICHT alle Rollen und Channels erstellen! \n'
                                 'Melde dich bei G3bE#6007 mit diesem Error\n' + str(e))
        return 1
    await serverchannel.send('Setup war erfolgreich!')

bot.run(TOKEN)
