import discord
import asyncio
import json
import time
import random
import requests
import io
import os, os.path, sys
import safygiphy
import logging
import secrets

logging.basicConfig(level=logging.INFO)

client = discord.Client()

TOKEN = secrets.TOKEN
MyID = secrets.MyID
PREFIX = secrets.PREFIX

g = safygiphy.Giphy()
times = time.time()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(activity=discord.Game(name='Booting...'))
    await asyncio.sleep(2)
    await client.change_presence(activity=discord.Game(name='warte auf anweisungen'))


@client.event
async def on_message(message):

    # 
    if message.content.startswith(PREFIX):
        channel = message.channel
        # Einfacher test command
        if message.content.lower().startswith(PREFIX + 'test'):
            await channel.send('Wow, bin ich krass!')

        # lässt den bot 5 sec schlafen
        elif message.content.lower().startswith(PREFIX + 'sleep'):
            sleeping = 1
            await asyncio.sleep(5)
            sleeping = 0
            await channel.send('Aufgewacht!')

        # ein cf command mit reaktionen
        elif message.content.lower().startswith(PREFIX + 'coinflip'):
            choice = random.randint(1, 2)
            if choice == 1:
                await message.add_reaction('👨')
            elif choice == 2:
                await message.add_reaction('🎱')

        elif message.content.lower().startswith(PREFIX + 'game') and message.author.id == MyID:
            game = message.content[6:]
            await client.change_presence(activity=discord.Game(name=game))

        elif message.content.lower().startswith('sudo reboot') and message.author.id == MyID:
            os.system('python3 reboot.py')
            sys.exit([0])

        elif message.content.lower().startswith(PREFIX + 'patch'):
            args = message.content[6:]
            if args != '':
                if message.author.id == MyID:
                    version = message.content[7:-(len(message.content)-12)]
                    patch = message.content[12:]
                    for i in client.guilds:
                        botchannel = discord.utils.find(lambda r: r.name == "bot-commands", i.channels)
                        ePatch = discord.Embed(
                            title='Patch-Notes für Version ' + version,
                            color=0x206694,
                            description=patch)
                        ePatch.set_author(
                            name='Notes by ' + message.author.name,
                            icon_url=message.author.avatar_url
                        )

                        ePatch.set_footer(
                            text='Made by G3bE',
                            icon_url='http://g3be.bplaced.net/Files/Pictures/g3be.jpg'
                        )
                        await botchannel.send(embed=ePatch)

        elif message.content.lower().startswith(PREFIX + 'uptime'):
            await channel.send('Ich bin ' + str(int((time.time() - times) / 60 / 60)) + ' h und ' + str(int((time.time() - times) / 60)) + ' min seid dem letzten Patch online.')

        elif message.content.lower().startswith(PREFIX + 'gif'):
            gif_tag = message.content[5:]
            rgif = g.random(tag=str(gif_tag))
            try:
                response = requests.get(str(rgif.get("data", {}).get('image_original_url')), stream=True)
                await channel.send(file=discord.File(io.BytesIO(response.raw.read()), 'video.gif'))
            except:
                await channel.send('Kein GIF gefunden... :(')

        elif message.content.lower().startswith(PREFIX + 'help'):
            embed = discord.Embed(
                title='Was ich kann, etc.',
                color=0x206694,
                description='Prefix=\'' + PREFIX + '\' \n'
                                                   'Commands: \n' +
                            PREFIX + 'test - Ignoriert das einfach! \n' +
                            PREFIX + 'sleep - Bots müssen auch mal schlafen. \n' +
                            PREFIX + 'coinflip - Kopf oder Zahl? \n' +
                            PREFIX + 'uptime - Hilft niemandem wirklich. \n' +
                            PREFIX + 'gif - Alle lieben sie! Schreib was dahinter! \n' +
                            PREFIX + 'report {user mention} - meldet einen User. 3 Reports = mute! \n' +
                            PREFIX + 'server - Commands für den Server. \n' +
                            PREFIX + 'user - Commands für User. \n' +
                            PREFIX + 'pokewatch - Noch nicht fertig. Wird ein Discordspiel. \n' +
                            PREFIX + 'urbdict {Suche} - Suche was im Urban-Dictonary. \n' +
                            PREFIX + 'help - Dieser Command. \n \n'
                                     'Außerdem gibt es eine Join- und Leave-Message.'
            )
            embed.set_author(
                name='CaptianOverkill',
                icon_url='http://g3be.bplaced.net/Files/Pictures/CaptainOverkill.png'
            )

            embed.set_footer(
                text='Made by G3bE',
                icon_url='http://g3be.bplaced.net/Files/Pictures/g3be.jpg'
            )

            await channel.send(embed=embed)

        elif message.content.lower().startswith(PREFIX + 'server'):
            args = message.content[7:]
            if args == '':
                await channel.send('Argumente: \n'
                                  'date - gibt das Erstellungsdatum des Servers zurück. \n'
                                  'icon - gibt das Icon des Servers zurück.')
            elif args == ' icon':
                icon = message.guild.icon_url
                try:
                    await channel.send(icon)
                except:
                    await channel.send('Kein Icon da!')
            elif args == ' date':
                await channel.send(message.guild.created_at)

        elif message.content.lower().startswith(PREFIX + 'user'):
            args = message.content[5:]

            if args == '':
                await channel.send('Argumente: \n'
                                   'date - gibt das Erstellungsdatum deines Accounts zurück. \n'
                                   'icon - gibt das Icon des Server zurück.')
            elif args == ' icon':
                try:
                    arguser = discord.utils.find(lambda r: r.id == message.mentions[0].id, message.guild.members)
                    icon = arguser.avatar_url
                except IndexError:
                    icon = message.author.avatar_url
                await channel.send(icon)
            elif args == ' date':
                try:
                    arguser = discord.utils.find(lambda r: r.id == message.mentions[0].id, message.guild.members)
                except IndexError:
                    arguser = message.author
                await channel.send(arguser.created_at)

        elif message.content.lower().startswith(PREFIX + 'report'):
            trusted = discord.utils.find(lambda r: r.name == "trusted", message.author.roles)
            if get_cooldown_end(user_id=message.author.id):
                if trusted is not None:
                    ruser = discord.utils.find(lambda r: r.id == message.mentions[0].id, message.guild.members)
                    firstReport = discord.utils.find(lambda r: r.name == "firstReport", message.guild.roles)
                    secondReport = discord.utils.find(lambda r: r.name == "secondReport", message.guild.roles)
                    thirdReport = discord.utils.find(lambda r: r.name == "thirdReport", message.guild.roles)
                    muted = discord.utils.find(lambda r: r.name == "muted", message.guild.roles)
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
                        await channel.send('muted')
                        await ruser.send(
                            'Du wurdest auf ' + message.guild.name + ' gemuted. Bitte schreibe einen \nModerator oder Administrator an um unmuted zu werden!')
                    elif report_count == 3:
                        await channel.send('thirdReport')
                    elif report_count == 2:
                        await channel.send('secondReport')
                    elif report_count == 1:
                        await channel.send('firstReport')
                    set_report_cd(message.author.id)
                else:
                    await channel.send('Du brauchst die "trusted"-Rolle um jemanden zu reporten!')
            else:
                await channel.send('Warte eine Woche nachdem du einen User reportest hast!')

        elif message.content.lower().startswith(PREFIX + 'urbdict'):
            args = message.content[9:]
            await channel.send('https://www.urbandictionary.com/define.php?term=' + args)

        elif message.content.lower() == PREFIX + '':
            await channel.send('Ähm, was willst du mit leeren Commands erreichen?')

        elif message.content.lower().startswith(PREFIX + 'pokewatch'):
            await channel.sent('Diese Funktion ist leider noch nicht verfügbar!')


@client.event
async def on_member_join(member):
    serverchannel = member.guild.channels[1]
    msg = "{0} ist {1} beigetreten!".format(member.mention, member.guild.name)
    await serverchannel.send(content=msg)


@client.event
async def on_member_remove(member):
    serverchannel = member.guild.channels[1]
    msg = "{0} hat {1} tragischer Weise verlassen!".format(member.mention, member.guild.name)
    await serverchannel.send(content=msg)


@client.event
async def on_guild_join(guild):
    serverchannel = guild.channels[0]
    await serverchannel.send(content='Hey there! \nI am Captain Overkill with a B. \nIch werde nur schnell ein paar Rollen und Channels erstellen!')
    try:
        await guild.create_role(guild, name='firstReport')
        await guild.create_role(guild, name='secondReport')
        await guild.create_role(guild, name='thirdReport')
        await guild.create_role(guild, name='muted')
        await guild.create_role(guild, name='trusted')
        await guild.create_text_channel(name='bot-commands')
    except:
        await serverchannel.send('Ich konnte NICHT alle Rollen und Channels erstellen! \nLösche folgende Rollen und führe ' + PREFIX + 'crtRoles aus: \n')


def set_report_cd(user_id: int):
    user_id = str(user_id)
    if os.path.isfile("users.json"):
        try:
            with open('users.json', 'r') as fp:
                users = json.load(fp)
                users[user_id]['cooldwon_end'] = int(time.time()) + 604800
            with open('users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
        except KeyError:
            with open('users.json', 'r') as fp:
                users = json.load(fp)
            users[user_id] = {}
            users[user_id]['cooldwon_end'] = int(time.time()) + 604800
            with open('users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
    else:
        users = {user_id: {}}
        users[user_id]['cooldwon_end'] = int(time.time()) + 604800
        with open('users.json', 'w') as fp:
            json.dump(users, fp, sort_keys=True, indent=4)


def get_cooldown_end(user_id: int):
    user_id = str(user_id)
    if os.path.isfile('users.json'):
        with open('users.json', 'r') as fp:
            users = json.load(fp)
        ret_val = True
        try:
            if int(users[user_id]['cooldwon_end']) <= int(time.time()):
                ret_val = True
            else:
                ret_val = False
        except KeyError:
            ret_val = True
        return ret_val
    else:
        return True


client.run(TOKEN)
