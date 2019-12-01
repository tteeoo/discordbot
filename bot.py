# imports, some may not be needed
import discord
from discord.ext import commands
import asyncio
import aiohttp
import logging
import random
from itertools import cycle
import time
import json
import os
import random
from operator import itemgetter
from collections import OrderedDict
import socket
import datetime
import math
import sys
import platform
from discord import Permissions
import praw
#import dbl
from decimal import Decimal

sys.setrecursionlimit(100000) # prevents stackoverlows (messy code)
TOKEN = 'NjUwNDc3MTY4NzAyMjU5MjIw.XeL6MA.C4hciy-hs4eO85ATT4gjgcxVClo' # sets discord bot token
os.chdir(r'/home/theodore/discordbot') # changes working directory (to load .json)
bot = commands.Bot(command_prefix = ".") # sets bot prefix
bot.remove_command('help') # removes default help command, so we can make our own

@bot.event
async def on_ready():
    print('rngBot is online! Running on: {} servers'.format(str(len(bot.servers))))
    await bot.change_presence(game=discord.Game(name='.help on ' + str(len(bot.servers)) + ' servers'))
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(DiscordBotsOrgAPI(bot))

#on sent
@bot.event
async def on_message(message):
    server = message.server
    channel = message.channel
    author = message.author
    content = message.content
    with open('servers.json', 'r') as f:
        servers = json.load(f)
    global bot
    if(server.id not in servers):
        servers[server.id] = {}
        servers[server.id]['prefix'] = '.'
    print('Message sent: {}: {}: {}: {}'.format(server, channel, author, content))
    await bot.process_commands(message)
    with open('users.json', 'r') as f:
        users = json.load(f)
    if(author.id in users):
        if(users[author.id]['points'] == 0):
            e = 20
        else:
            e = round(2 / users[author.id]['points'] * 20 + 1)
        await add_points(users, message.author, e)
    with open('users.json', 'w') as f:
        json.dump(users, f)
    with open('servers.json', 'w') as f:
        json.dump(servers, f)

#on delete
@bot.event
async def on_message_delete(message):
    server = message.server
    channel = message.channel
    author = message.author
    content = message.content
    print('Message deleted: {}: {}: {}: {}'.format(server, channel, author, content))

#update_data
async def update_data(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]['points'] = 500
        users[user.id]['total'] = 500

#add_points
async def add_points(users, user, pnts):
    users[user.id]['points'] += pnts
    users[user.id]['total'] += pnts

#bal
@bot.command(pass_context=True)
async def bal(ctx):
    user = ctx.message.author
    with open('users.json', 'r') as f:
        users = json.load(f)

    if not user.id in users:
        await update_data(users, ctx.message.author)
    point = users[user.id]['points']
    if int(point) > 999999999999999999999999999999:
        point = "{:.2e}".format(Decimal(point))
    total = users[user.id]['total']
    if int(total) > 999999999999999999999999999999:
        total = "{:.2e}".format(Decimal(total))
    await bot.say('{}, you have {} points and {} total earnings'.format(user.mention, point, total))

    with open('users.json', 'w') as f:
        json.dump(users, f)

#clear
@bot.command(pass_context = True)
async def clear(ctx, amount=1):
    user = ctx.message.author
    if("staff" in [y.name.lower() for y in user.roles]):
        channel = ctx.message.channel
        messages = []
        async for message in bot.logs_from(channel, limit=int(amount)):
            messages.append(message)
        await bot.delete_messages(messages)
        await bot.say('Messages deleted succesfully!')
    else:
        await bot.say('{}, Error 403'.format(user.mention))

#debug
@bot.command(pass_context=True)
async def debug(ctx, debugparams):
    user = ctx.message.author
    server = ctx.message.server
    with open('users.json', 'r') as f:
        users = json.load(f)
    with open('servers.json', 'r') as f:
        servers = json.load(f)
    if(ctx.message.author.id == '258771223473815553'):
        await bot.say('Results: {}'.format(eval(debugparams)))
    else:
        await bot.say('Error code 403')
    with open('users.json', 'w') as f:
        json.dump(users, f)
    with open('servers.json', 'w') as f:
        json.dump(servers, f)

#rng
@bot.command(pass_context=True)
async def rng(ctx, e, a):
    user = ctx.message.author
    try:
        i = random.randint(int(e), int(a))
        await bot.say('{}, your random number is: {}'.format(user.mention, str(i)))
    except:
        await bot.say('{}, please enter an integer, then a another integer greater than the other.'.format(user.mention))

#give
@bot.command(pass_context=True)
async def give(ctx, amount, user: discord.Member):
    with open('users.json', 'r') as f:
        users = json.load(f)
    author = ctx.message.author
    if(ctx.message.author.id == '258771223473815553'):
        users[user.id]['points']+= int(amount)
        users[user.id]['total']+= int(amount)
        await bot.say('{}, gave {} points to {}'.format(author.mention, amount, user.mention))
    else:
        await bot.say('Error code 403')
    with open('users.json', 'w') as f:
         json.dump(users, f)

#lookup
@bot.command(pass_context=True)
async def lookup(ctx, user: discord.Member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    point = users[user.id]['points']
    if int(point) > 999999999999999999999999999999:
        point = "{:.2e}".format(Decimal(point))
    total = users[user.id]['total']
    if int(total) > 999999999999999999999999999999:
        total = "{:.2e}".format(Decimal(total))
    await bot.say('{}, {} has {} points and {} total earnings'.format(ctx.message.author.mention, user.mention, point, total))

    with open('users.json', 'w') as f:
        json.dump(users, f)

#flip
@bot.command(pass_context=True)
async def flip(ctx, amnt):
    user = ctx.message.author
    if(int(amnt)>0):
        user = ctx.message.author
        with open('users.json', 'r') as f:
            users = json.load(f)
        if not user.id in users:
            await update_data(users, ctx.message.author)
        e = random.randint(1,2)
        if(int(amnt)<=users[user.id]['points']):
            if(e == 1):
                users[user.id]['points'] += int(amnt)
                users[user.id]['total'] += int(amnt)
                await bot.say('{}, you won {} points'.format(user.mention, amnt))
            else:
                users[user.id]['points'] -= int(amnt)
                await bot.say('{}, you lost {} points'.format(user.mention, amnt))
            with open('users.json', 'w') as f:
                json.dump(users, f)
        else:
            await bot.say("{}, you don't have enough points to do that".format(user.mention))
    else:
        await bot.say("{}, you can only flip integers greater than 0".format(user.mention))


#flip3
@bot.command(pass_context=True)
async def flip3(ctx, amnt):
    user = ctx.message.author
    if(int(amnt)>0):
        with open('users.json', 'r') as f:
            users = json.load(f)
        if not user.id in users:
            await update_data(users, ctx.message.author)
        e = random.randint(1,4)
        if(int(amnt)<=users[user.id]['points']):
            if(e == 1):
                users[user.id]['points'] += round(int(amnt) / 3)
                users[user.id]['total'] += round(int(amnt) / 3)
                await bot.say('{}, you won {} points'.format(user.mention, round(int(amnt) / 3)))
            if(e == 2):
                users[user.id]['points'] += round(int(amnt) / 3)
                users[user.id]['total'] += round(int(amnt) / 3)
                await bot.say('{}, you won {} points'.format(user.mention, round(int(amnt) / 3)))
            if(e == 3):
                users[user.id]['points'] += round(int(amnt) / 3)
                users[user.id]['total'] += round(int(amnt) / 3)
                await bot.say('{}, you won {} points'.format(user.mention, round(int(amnt) / 3)))
            if(e == 4):
                users[user.id]['points'] -= int(amnt)
                await bot.say('{}, you lost {} points'.format(user.mention, amnt))
            with open('users.json', 'w') as f:
                 json.dump(users, f)
        else:
            await bot.say("{}, you don't have enough points to do that".format(user.mention))
    else:
        await bot.say("{}, you can only flip integers greater than 0".format(user.mention))

#flip2
@bot.command(pass_context=True)
async def flip2(ctx, amnt):
    user = ctx.message.author
    if(int(amnt)>0):
        with open('users.json', 'r') as f:
            users = json.load(f)
        if not user.id in users:
            await update_data(users, ctx.message.author)
        e = random.randint(1,10)
        if(int(amnt) * int(amnt) > 999999999999999999999999999999):
            winnings = str("{:.2e}".format(Decimal(int(amnt) * int(amnt))))
        else:
            winnings = str(int(amnt) * int(amnt))
        if(int(amnt)<=users[user.id]['points']):
            if(e == 1):
                users[user.id]['points'] += int(amnt) * int(amnt)
                users[user.id]['total'] += int(amnt) * int(amnt)
                await bot.say('{}, you won {} points'.format(user.mention, winnings))
            else:
                if(int(amnt) * int(amnt) < users[user.id]['points']):
                    users[user.id]['points'] -= int(amnt) * int(amnt)
                    await bot.say('{}, you lost {} points'.format(user.mention, winnings))
                else:
                    users[user.id]['points'] = 0
                    await bot.say('{}, you lost {} points'.format(user.mention, winnings))
            with open('users.json', 'w') as f:
                json.dump(users, f)
        else:
            await bot.say("{}, you don't have enough points to do that".format(user.mention))
    else:
        await bot.say("{}, you can only flip integers greater than 0".format(user.mention))

#ping
@bot.command(pass_context=True)
async def ping(ctx):
    user = ctx.message.author
    t = await bot.say(user.mention + ',')
    ms = (t.timestamp-ctx.message.timestamp).total_seconds() * 1000
    await bot.edit_message(t, new_content="{} rngBot's latency is: {}ms".format(user.mention, int(ms)))

#pay
@bot.command(pass_context=True)
async def pay(ctx, amnt, member: discord.Member):
    user = ctx.message.author
    if(int(amnt)>0):
        user = ctx.message.author
        with open('users.json', 'r') as f:
            users = json.load(f)
        if not user.id in users:
            await update_data(users, ctx.message.author)
        if(int(amnt)<=users[user.id]['points']):
            users[ctx.message.author.id]['points'] -= int(amnt)
            users[member.id]['points'] += int(amnt)
            users[member.id]['total'] += int(amnt)

            await bot.say("{}, you paid {} {} points".format(user.mention, member.mention, amnt))

            with open('users.json', 'w') as f:
                json.dump(users, f)
        else:
            await bot.say("{}, you don't have enough points to do that".format(user.mention))
    else:
        await bot.say("{}, you can only pay integers greater than 0".format(user.mention))

#top
@bot.command(pass_context=True)
async def top(ctx):
    user = ctx.message.author
    with open('users.json', 'r') as f:
        users = json.load(f)
    order2 = sorted(users.items(), key=lambda val: val[1]['points'], reverse=True)
    firstp = str(order2[0])[2:]
    x = 0
    while(1==1):
        if (firstp[x] == "'"):
            break
        x+=1
    firstp = str(order2[0])[2:x+2]
    firsts = users[firstp]['points']
    if int(firsts) > 999999999999999999999999999999:
        firsts = "{:.2e}".format(Decimal(firsts))

    secondp = str(order2[1])[2:]
    x = 0
    while(1==1):
        if (secondp[x] == "'"):
            break
        x+=1
    secondp = str(order2[1])[2:x+2]
    seconds = users[secondp]['points']
    if int(seconds) > 999999999999999999999999999999:
        seconds = "{:.2e}".format(Decimal(seconds))

    thirdp = str(order2[2])[2:]
    x = 0
    while(1==1):
        if (thirdp[x] == "'"):
            break
        x+=1
    thirdp = str(order2[2])[2:x+2]
    thirds = users[thirdp]['points']
    if int(thirds) > 999999999999999999999999999999:
        thirds = "{:.2e}".format(Decimal(thirds))

    fourthp = str(order2[3])[2:]
    x = 0
    while(1==1):
        if (fourthp[x] == "'"):
            break
        x+=1
    fourthp = str(order2[3])[2:x+2]
    fourths = users[fourthp]['points']
    if int(fourths) > 999999999999999999999999999999:
        fourths = "{:.2e}".format(Decimal(fourths))

    fivep = str(order2[4])[2:]
    x = 0
    while(1==1):
        if (fivep[x] == "'"):
            break
        x+=1
    fivep = str(order2[4])[2:x+2]
    fives = users[fivep]['points']
    if int(fives) > 999999999999999999999999999999:
        fives = "{:.2e}".format(Decimal(fives))

    await bot.say("{}, The top players are: \n \n {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points```".format(user.mention, '<@' + firstp + '>', firsts, '<@' + secondp + '>',  seconds, '<@' + thirdp + '>', thirds, '<@' + fourthp + '>', fourths, '<@' + fivep + '>', fives))

    with open('users.json', 'w') as f:
        json.dump(users, f)

#servertop
@bot.command(pass_context=True)
async def servertop(ctx):
    user = ctx.message.author
    server = ctx.message.server
    with open('users.json', 'r') as f:
        users = json.load(f)
    q=0
    serverMem = list()
    serverPoints = list()
    d = dict()
    for member in server.members:
        if(member.id in users):
            serverMem.append(member.id)
    for x in serverMem:
        serverPoints.append(users[x]['points'])
    while(int(q)<int(len(serverMem))):
        d.update( {str(serverMem[q]) : int(serverPoints[q])} )
        q=q+1
    order2 = sorted(d.items(), key=lambda val: val[1], reverse=True)
    firstp = str(order2[0])[2:]
    x = 0
    while(1==1):
        if (firstp[x] == "'"):
            break
        x+=1
    firstp = str(order2[0])[2:x+2]
    firsts = users[firstp]['points']
    if int(firsts) > 999999999999999999999999999999:
        firsts = "{:.2e}".format(Decimal(firsts))

    secondp = str(order2[1])[2:]
    x = 0
    while(1==1):
        if (secondp[x] == "'"):
            break
        x+=1
    secondp = str(order2[1])[2:x+2]
    seconds = users[secondp]['points']
    if int(seconds) > 999999999999999999999999999999:
        seconds = "{:.2e}".format(Decimal(seconds))

    if(len(order2)>=3):
        thirdp = str(order2[2])[2:]
        x = 0
        while(1==1):
            if (thirdp[x] == "'"):
                break
            x+=1
        thirdp = str(order2[2])[2:x+2]
        thirds = users[thirdp]['points']
        if int(thirds) > 999999999999999999999999999999:
            thirds = "{:.2e}".format(Decimal(thirds))

    if(len(order2)>=4):
        fourthp = str(order2[3])[2:]
        x = 0
        while(1==1):
            if (fourthp[x] == "'"):
                break
            x+=1
        fourthp = str(order2[3])[2:x+2]
        fourths = users[fourthp]['points']
        if int(fourths) > 999999999999999999999999999999:
            fourths = "{:.2e}".format(Decimal(fourths))

    if(len(order2)>=5):
        fivep = str(order2[4])[2:]
        x = 0
        while(1==1):
            if (fivep[x] == "'"):
                break
            x+=1
        fivep = str(order2[4])[2:x+2]
        fives = users[fivep]['points']
        if int(fives) > 999999999999999999999999999999:
            fives = "{:.2e}".format(Decimal(fives))
    try:
        if(len(order2)==2):
            await bot.say("{}, The top players on your server are: \n \n {} ```{} points``` {} ```{} points```".format(user.mention, '<@' + firstp + '>', firsts, '<@' + secondp + '>',  seconds))
        if(len(order2)==3):
            await bot.say("{}, The top players on your server are: \n \n {} ```{} points``` {} ```{} points``` {} ```{} points```".format(user.mention, '<@' + firstp + '>', firsts, '<@' + secondp + '>',  seconds, '<@' + thirdp + '>', thirds))
        if(len(order2)==4):
            await bot.say("{}, The top players on your server are: \n \n {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points```".format(user.mention, '<@' + firstp + '>', firsts, '<@' + secondp + '>',  seconds, '<@' + thirdp + '>', thirds, '<@' + fourthp + '>', fourths))
        if(len(order2)>=5):
            await bot.say("{}, The top players on your server are: \n \n {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points```".format(user.mention, '<@' + firstp + '>', firsts, '<@' + secondp + '>',  seconds, '<@' + thirdp + '>', thirds, '<@' + fourthp + '>', fourths, '<@' + fivep + '>', fives))

    except KeyError:
        await bot.say("KeyError")
    except HTTPException:
        await bot.say("HTTPException")

    with open('users.json', 'w') as f:
        json.dump(users, f)

#help
@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.purple()
    )

    embed.set_author(name='rngBot commands')
    embed.add_field(name='.bal', value="Shows your current balance.",inline=False)
    embed.add_field(name='.pay (amount) (person)', value='Pays an amount of points to a person',inline=False)
    embed.add_field(name='.lookup (person)', value="Looks up a different person's balance",inline=False)
    embed.add_field(name='.ping', value="Checks rngBot's latency",inline=False)
    embed.add_field(name='.top', value="Shows the top 5 players",inline=False)
    embed.add_field(name='.servertop', value="Shows the top 5 players just on your server",inline=False)
    embed.add_field(name='.flip (amount)', value='Flips a coin to decide if you win or lose an amount of points (1/2) win chance)',inline=False)
    embed.add_field(name='.flip2 (amount)', value='Flips a 10-sided coin to decide if you win or lose the squared amount of points (1/10 win chance)',inline=False)
    embed.add_field(name='.flip3 (amount)', value='Flips a 4-sided coin to decide if you win the amount of points divided by 3 or lose the amount of points (3/4 win chance)',inline=False)

    await bot.send_message(author, embed=embed)
    await bot.send_message(ctx.message.channel, "{}, you've been DMed the help message, if you didn't get it, make sure you can get DM messages from non-friends".format(author.mention))

bot.run(TOKEN)
