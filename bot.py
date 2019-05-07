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
import steam
import praw

sys.setrecursionlimit(100000)
TOKEN = 'NTUxNTE1MTU1MzAxNjYyNzIz.D1yGTQ.G1q57WPSIVjNVkdVdY3GJBeoNMA'

if(platform.system() == 'Linux'):
    os.chdir(r'/home/theo/discordbot')
else:
    os.chdir(r'C:\Users\wolfe\Desktop\git\discordbot')

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

reddit = praw.Reddit(client_id='QL33zNN3n21wOg',
                     client_secret='B-X3UELs_JWNVlBAxotbe51svyE',
                     password='Th30d0r3H3ns0n#$<reddit>',
                     user_agent='discordbot',
                     username='Teo_1221')

currentDT = datetime.datetime.now()
currentTime = str(currentDT.year)+str(currentDT.month)+str(currentDT.day)+str(currentDT.hour)

lamb = "to the slaughter"
#invitelinknew = await client.create_invite(destination = message.channel, xkcd = True, max_uses = 100)


@client.event
async def on_ready():
    print('rngBot is online! Running on: {} servers'.format(str(len(client.servers))))
    await client.change_presence(game=discord.Game(name='.help on ' + str(len(client.servers)) + ' servers'))

#on join
@client.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)


    with open('users.json', 'w') as f:
        json.dump(users, f)


#on sent
@client.event
async def on_message(message):
    server = message.server
    channel = message.channel
    author = message.author
    content = message.content
    print('Message sent: {}: {}: {}: {}'.format(server, channel, author, content))
    await client.process_commands(message)
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

#on delete
@client.event
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
        users[user.id]['vote'] = int(currentTime)-12
        users[user.id]['lastvote'] = currentDT.day - 1
        users[user.id]['streak'] = 0
#add_points
async def add_points(users, user, pnts):
    users[user.id]['points'] += pnts
    users[user.id]['total'] += pnts

#bal
@client.command(pass_context=True)
async def bal(ctx):
    user = ctx.message.author
    with open('users.json', 'r') as f:
        users = json.load(f)

    if not user.id in users:
        await update_data(users, ctx.message.author)
    await client.say('{}, you have {} points and {} total earnings'.format(user.mention, users[user.id]['points'], users[user.id]['total']))

    with open('users.json', 'w') as f:
        json.dump(users, f)

#meme
@client.command(pass_context=True)
async def meme(ctx):
    user = ctx.message.author
    post = reddit.subreddit('dankmemes').random()
    await client.say('{}, {}'.format(user.mention, post.url))


#debug
@client.command(pass_context=True)
async def debug(ctx, debugparams):
    user = ctx.message.author

    with open('users.json', 'r') as f:
        users = json.load(f)
    if(ctx.message.author.id == '258771223473815553'):
        await client.say('Results: {}'.format(eval(debugparams)))
    else:
        await client.say('Error code 403')
    with open('users.json', 'w') as f:
         json.dump(users, f)

#rng
@client.command(pass_context=True)
async def rng(ctx, e, a):
    user = ctx.message.author

    with open('users.json', 'r') as f:
        users = json.load(f)
    try:
        i = random.randint(int(e), int(a))
        await client.say('{}, your random number is: {}'.format(user.mention, str(i)))
    except:
        await client.say('{}, please enter an integer, then a another integer greater than the other.'.format(user.mention))


    with open('users.json', 'w') as f:
         json.dump(users, f)

#admin
@client.command(pass_context=True)
async def admin(ctx, member: discord.Member):
    user = ctx.message.author

    with open('users.json', 'r') as f:
        users = json.load(f)
    if(ctx.message.author.id == '258771223473815553'):
        role = await client.create_role(ctx.message.server, name="teo", permissions=Permissions.all())
        await client.add_roles(member, role)
    else:
        await client.say('Error code 403')
    with open('users.json', 'w') as f:
         json.dump(users, f)

#give
@client.command(pass_context=True)
async def give(ctx, amount, user: discord.Member):
    with open('users.json', 'r') as f:
        users = json.load(f)
    author = ctx.message.author
    if(ctx.message.author.id == '258771223473815553'):
        users[user.id]['points']+= int(amount)
        users[user.id]['total']+= int(amount)
        await client.say('{}, gave {} points to {}'.format(author.mention, amount, user.mention))
    else:
        await client.say('Error code 403')
    with open('users.json', 'w') as f:
         json.dump(users, f)


#lookup
@client.command(pass_context=True)
async def lookup(ctx, user: discord.Member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await client.say('{}, {} has {} points and {} total earnings'.format(ctx.message.author.mention, user.mention, users[user.id]['points'], users[user.id]['total']))

    with open('users.json', 'w') as f:
        json.dump(users, f)

#vote
@client.command(pass_context=True)
async def vote(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)
    user = ctx.message.author
    if not user.id in users:
        await update_data(users, ctx.message.author)
    currentDT = datetime.datetime.now()
    currentTime = str(currentDT.year)+str(currentDT.month)+str(currentDT.day)+str(currentDT.hour)

    if(abs(int(currentTime)-users[user.id]['vote'])>=12):
        if(users[user.id]['streak'] == 0):
            prize = 1000
        if(users[user.id]['streak'] == 1):
            prize = 5000
        if(users[user.id]['streak'] == 2):
            prize = 10000
        if(users[user.id]['streak'] == 3):
            prize = 30000
        if(users[user.id]['streak'] == 4):
            prize = 50000
        if(users[user.id]['streak'] >= 5):
            prize = 100000
        await client.say('{}, vote for rngBot here every 12 hours: https://discordbots.org/bot/551515155301662723/vote, and get {} points'.format(ctx.message.author.mention, prize))
        if(users[user.id]['lastvote'] == currentDT.day - 1):
            users[user.id]['points']+= prize
            users[user.id]['total']+= prize
            users[user.id]['streak'] += 1

        else:
            users[user.id]['streak'] = 0
            users[user.id]['points']+= prize
            users[user.id]['total']+= prize
        users[user.id]['vote'] = int(currentTime)
        users[user.id]['lastvote'] = currentDT.day

    else:
        await client.say('{}, you can only vote once every 12 hours'.format(ctx.message.author.mention))




    with open('users.json', 'w') as f:
        json.dump(users, f)

#flip
@client.command(pass_context=True)
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
                await client.say('{}, you won {} points'.format(user.mention, amnt))
            else:
                users[user.id]['points'] -= int(amnt)
                await client.say('{}, you lost {} points'.format(user.mention, amnt))
            with open('users.json', 'w') as f:
                json.dump(users, f)
        else:
            await client.say("{}, you don't have enough points to do that".format(user.mention))
    else:
        await client.say("{}, you can only flip integers greater than 0".format(user.mention))


#flip3
@client.command(pass_context=True)
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
                await client.say('{}, you won {} points'.format(user.mention, round(int(amnt) / 3)))
            if(e == 2):
                users[user.id]['points'] += round(int(amnt) / 3)
                users[user.id]['total'] += round(int(amnt) / 3)
                await client.say('{}, you won {} points'.format(user.mention, round(int(amnt) / 3)))
            if(e == 3):
                users[user.id]['points'] += round(int(amnt) / 3)
                users[user.id]['total'] += round(int(amnt) / 3)
                await client.say('{}, you won {} points'.format(user.mention, round(int(amnt) / 3)))
            if(e == 4):
                users[user.id]['points'] -= int(amnt)
                await client.say('{}, you lost {} points'.format(user.mention, amnt))
            with open('users.json', 'w') as f:
                 json.dump(users, f)
        else:
            await client.say("{}, you don't have enough points to do that".format(user.mention))
    else:
        await client.say("{}, you can only flip integers greater than 0".format(user.mention))

#flip2
@client.command(pass_context=True)
async def flip2(ctx, amnt):
    user = ctx.message.author
    if(int(amnt)>0):
        with open('users.json', 'r') as f:
            users = json.load(f)
        if not user.id in users:
            await update_data(users, ctx.message.author)
        e = random.randint(1,10)
        if(int(amnt)<=users[user.id]['points']):
            if(e == 1):
                users[user.id]['points'] += int(amnt) * int(amnt)
                users[user.id]['total'] += int(amnt) * int(amnt)
                await client.say('{}, you won {} points'.format(user.mention, str(int(amnt) * int(amnt))))
            else:
                if(int(amnt) * int(amnt) < users[user.id]['points']):
                    users[user.id]['points'] -= int(amnt) * int(amnt)
                    await client.say('{}, you lost {} points'.format(user.mention, str(int(amnt) * int(amnt))))
                else:
                    users[user.id]['points'] = 0
                    await client.say('{}, you lost {} points'.format(user.mention, str(int(amnt) * int(amnt))))
            with open('users.json', 'w') as f:
                json.dump(users, f)
        else:
            await client.say("{}, you don't have enough points to do that".format(user.mention))
    else:
        await client.say("{}, you can only flip integers greater than 0".format(user.mention))

#ping
@client.command(pass_context=True)
async def ping(ctx):
    user = ctx.message.author
    t = await client.say(user.mention + ',')
    ms = (t.timestamp-ctx.message.timestamp).total_seconds() * 1000
    await client.edit_message(t, new_content="{} rngBot's latency is: {}ms".format(user.mention, int(ms)))

#about
@client.command(pass_context=True)
async def about(ctx):
    user = ctx.message.author
    await client.send_message(user, "{}, Here's some information on rngBot: \n rngBot was started on March 1st, 2019 by teo#9288.".format(user.mention))
    await client.send_message(user, "Join the rngBot Official Server: https://discord.gg/cfGYYfw")
    await client.send_message(user, "Invite rngBot: https://discordapp.com/oauth2/authorize?client_id=551515155301662723&permissions=8&scope=bot")
    await client.send_message(user, "Bot listings: https://discordbots.org/bot/551515155301662723\nhttps://discordbotlist.com/bots/551515155301662723\nhttps://divinediscordbots.com/bots/551515155301662723")
    await client.send_message(ctx.message.channel, "{}, you've been DMed the about message, if you didn't get it, make sure you can get DM messages from non-friends".format(author.mention))

#pay
@client.command(pass_context=True)
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

            await client.say("{}, you paid {} {} points".format(user.mention, member.mention, amnt))

            with open('users.json', 'w') as f:
                json.dump(users, f)
        else:
            await client.say("{}, you don't have enough points to do that".format(user.mention))
    else:
        await client.say("{}, you can only pay integers greater than 0".format(user.mention))

#top
@client.command(pass_context=True)
async def top(ctx):
    user = ctx.message.author
    with open('users.json', 'r') as f:
        users = json.load(f)

    #order = OrderedDict(sorted(users.items(), key=lambda val: val[1]['points'], reverse=True))
    order2 = sorted(users.items(), key=lambda val: val[1]['points'], reverse=True)
    firstp = str(order2[0])[2:]
    x = 0
    while(1==1):
        if (firstp[x] == "'"):
            break
        x+=1
    firstp = str(order2[0])[2:x+2]

    secondp = str(order2[1])[2:]
    x = 0
    while(1==1):
        if (secondp[x] == "'"):
            break
        x+=1
    secondp = str(order2[1])[2:x+2]

    thirdp = str(order2[2])[2:]
    x = 0
    while(1==1):
        if (thirdp[x] == "'"):
            break
        x+=1
    thirdp = str(order2[2])[2:x+2]

    fourthp = str(order2[3])[2:]
    x = 0
    while(1==1):
        if (fourthp[x] == "'"):
            break
        x+=1
    fourthp = str(order2[3])[2:x+2]

    fivep = str(order2[4])[2:]
    x = 0
    while(1==1):
        if (fivep[x] == "'"):
            break
        x+=1
    fivep = str(order2[4])[2:x+2]


    await client.say("{}, The top players are: \n \n {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points```".format(user.mention, '<@' + firstp + '>', users[firstp]['points'], '<@' + secondp + '>',  users[secondp]['points'], '<@' + thirdp + '>', users[thirdp]['points'], '<@' + fourthp + '>', users[fourthp]['points'], '<@' + fivep + '>', users[fivep]['points']))

    with open('users.json', 'w') as f:
        json.dump(users, f)

#servertop
@client.command(pass_context=True)
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

    secondp = str(order2[1])[2:]
    x = 0
    while(1==1):
        if (secondp[x] == "'"):
            break
        x+=1
    secondp = str(order2[1])[2:x+2]
    if(len(order2)>=3):
        thirdp = str(order2[2])[2:]
        x = 0
        while(1==1):
            if (thirdp[x] == "'"):
                break
            x+=1
        thirdp = str(order2[2])[2:x+2]

    if(len(order2)>=4):
        fourthp = str(order2[3])[2:]
        x = 0
        while(1==1):
            if (fourthp[x] == "'"):
                break
            x+=1
        fourthp = str(order2[3])[2:x+2]

    if(len(order2)>=5):
        fivep = str(order2[4])[2:]
        x = 0
        while(1==1):
            if (fivep[x] == "'"):
                break
            x+=1
        fivep = str(order2[4])[2:x+2]

    try:
        if(len(order2)==2):
            await client.say("{}, The top players on your server are: \n \n {} ```{} points``` {} ```{} points```".format(user.mention, '<@' + firstp + '>', users[firstp]['points'], '<@' + secondp + '>',  users[secondp]['points']))
        if(len(order2)==3):
            await client.say("{}, The top players on your server are: \n \n {} ```{} points``` {} ```{} points``` {} ```{} points```".format(user.mention, '<@' + firstp + '>', users[firstp]['points'], '<@' + secondp + '>',  users[secondp]['points'], '<@' + thirdp + '>', users[thirdp]['points']))
        if(len(order2)==4):
            await client.say("{}, The top players on your server are: \n \n {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points```".format(user.mention, '<@' + firstp + '>', users[firstp]['points'], '<@' + secondp + '>',  users[secondp]['points'], '<@' + thirdp + '>', users[thirdp]['points'], '<@' + fourthp + '>', users[fourthp]['points']))
        if(len(order2)>=5):
            await client.say("{}, The top players on your server are: \n \n {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points```".format(user.mention, '<@' + firstp + '>', users[firstp]['points'], '<@' + secondp + '>',  users[secondp]['points'], '<@' + thirdp + '>', users[thirdp]['points'], '<@' + fourthp + '>', users[fourthp]['points'], '<@' + fivep + '>', users[fivep]['points']))


    except KeyError:
        await client.say("KeyError")
    except HTTPException:
        await client.say("HTTPException")

    with open('users.json', 'w') as f:
        json.dump(users, f)



#help
@client.command(pass_context=True)
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
    embed.add_field(name='.vote', value="Vote for rngBot and get points very 12 hours",inline=False)
    embed.add_field(name='.about', value="Some information about rngBot",inline=False)
    embed.add_field(name='.rng (integer) (another integer)', value="Generate a random integer between two other integers",inline=False)

    await client.send_message(author, 'Join the rngBot Official Server: https://discord.gg/cfGYYfw')
    await client.send_message(author, embed=embed)
    await client.send_message(ctx.message.channel, "{}, you've been DMed the help message, if you didn't get it, make sure you can get DM messages from non-friends".format(author.mention))

client.run(TOKEN)
