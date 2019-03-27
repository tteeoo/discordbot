import discord
from discord.ext import commands
import asyncio
import aiohttp
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

sys.setrecursionlimit(100000)
TOKEN = 'NTUxNTE1MTU1MzAxNjYyNzIz.D1yGTQ.G1q57WPSIVjNVkdVdY3GJBeoNMA'
os.chdir(r'/home/theo/discordbot')
#os.chdir(r'C:\Users\wolfe\Desktop\git\discordbot')

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

penis = 'long'
sam = 'pussy boi'
currentDT = datetime.datetime.now()
currentTime = str(currentDT.year)+str(currentDT.month)+str(currentDT.day)+str(currentDT.hour)

@client.event
async def on_ready():
    print('rngBot is online! Running on: {} servers'.format(str(len(client.servers))))
    await client.change_presence(game=discord.Game(name='.help on ' + str(len(client.servers)) + ' servers'))

#on join
@client.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

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
    if(message.content.startswith('.')):
            await update_data(users, message.author)
    else:
        await update_data(users, message.author)
        if(users[author.id]['points'] == 0):
            e = 20
        else:
            e = round(2 / users[author.id]['points'] * 20 + 1)
        await add_points(users, message.author, e)

    #if(users['lottery']['start'] == int(currentTime)-12):
    #    entered=users['lottery']['entered'].split(" ")
    #    selected = random.randint(0,len(entered))
    #    winner=entered[selected]
    #    await client.send_message(winner, "You won the lottery for {} points".format(str(users['lottery']['pot'])))
    #    users[winner]['points']+=users['lottery']['pot']
    #    users['lottery']['start']=currentTime

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
    if not 'vote' in users[user.id]:
        users[user.id]['vote'] = int(currentTime)-12
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

    await client.say('{}, you have {} points and {} total earnings'.format(user.mention, users[user.id]['points'], users[user.id]['total']))

    with open('users.json', 'w') as f:
        json.dump(users, f)

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

#give
@client.command(pass_context=True)
async def give(ctx, amount, user: discord.Member):
    with open('users.json', 'r') as f:
        users = json.load(f)
    author = ctx.message.author
    if author.id==258771223473615553
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

#lottery
#@client.command(pass_context=True)
#async def lottery(ctx, joined):
#    with open('users.json', 'r') as f:
#        users = json.load(f)
#    user = ctx.message.author
#    entered=users['lottery']['entered'].split(" ")
#
#    if(joined == "join"):
#        if(500<=users[user.id]['points']):
#            users[user.id]['points']-= 500
#            users['lottery']['pot']+= 500
#            users['lottery']['entered'] + user.id
#            await client.say('{}, you joined the lottery for 500 points'.format(ctx.message.author.mention))
#
#        else:
#            await client.say("{}, you don't have enough points to do that".format(user.mention))
#
#    if(joined == "status"):
#        await client.say('{}, the lottery currently has {} entered users and the winnings are {}'.format(ctx.message.author.mention, len(entered), users['lottery']['pot']))
#
#    with open('users.json', 'w') as f:
#        json.dump(users, f)

#vote
@client.command(pass_context=True)
async def vote(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)
    user = ctx.message.author
    currentDT = datetime.datetime.now()
    currentTime = str(currentDT.year)+str(currentDT.month)+str(currentDT.day)+str(currentDT.hour)

    if(abs(int(currentTime)-users[user.id]['vote'])>=12):
        await client.say('{}, vote for rngBot here every 12 hours: https://discordbots.org/bot/551515155301662723/vote, and get 5000 points'.format(ctx.message.author.mention))
        users[user.id]['points']+= 5000
        users[user.id]['total']+= 5000
        users[user.id]['vote'] = int(currentTime)

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


#pay
@client.command(pass_context=True)
async def pay(ctx, amnt, member: discord.Member):
    user = ctx.message.author
    if(int(amnt)>0):
        user = ctx.message.author
        with open('users.json', 'r') as f:
            users = json.load(f)
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


    await client.say("{}, The top players on your server are: \n \n {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points```".format(user.mention, '<@' + firstp + '>', users[firstp]['points'], '<@' + secondp + '>',  users[secondp]['points'], '<@' + thirdp + '>', users[thirdp]['points'], '<@' + fourthp + '>', users[fourthp]['points'], '<@' + fivep + '>', users[fivep]['points']))

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
    embed.add_field(name='.bal', value='Shows your current balance',inline=False)
    embed.add_field(name='.pay (amount) (person)', value='Pays an amount of points to a person',inline=False)
    embed.add_field(name='.lookup (person)', value="Looks up a different person's balance",inline=False)
    embed.add_field(name='.ping', value="Checks rngBot's latency",inline=False)
    embed.add_field(name='.top', value="Shows the top 5 players",inline=False)
    embed.add_field(name='.servertop', value="Shows the top 5 players just on your server",inline=False)
    embed.add_field(name='.flip (amount)', value='Flips a coin to decide if you win or lose an amount of points (1/2) win chance)',inline=False)
    embed.add_field(name='.flip2 (amount)', value='Flips a 10-sided coin to decide if you win or lose the squared amount of points (1/10 win chance)',inline=False)
    embed.add_field(name='.flip3 (amount)', value='Flips a 4-sided coin to decide if you win the amount of points divided by 3 or lose the amount of points (3/4 win chance)',inline=False)
    embed.add_field(name='.vote', value="Vote for rngBot and get 5000 points very 12 hours",inline=False)
    embed.add_field(name='.about', value="Some information about rngBot",inline=False)

    await client.send_message(author, 'Join the rngBot Official Server: https://discord.gg/cfGYYfw')
    await client.send_message(author, embed=embed)
    await client.send_message(ctx.message.channel, "{}, you've been DMed the help message, if you didn't get it, make sure you can get DM messages from non-friends".format(author.mention))



client.run(TOKEN)
