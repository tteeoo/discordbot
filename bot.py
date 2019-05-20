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
import dbl
from googletrans import Translator
from decimal import Decimal

sys.setrecursionlimit(100000)
TOKEN = 'NTUxNTE1MTU1MzAxNjYyNzIz.D1yGTQ.G1q57WPSIVjNVkdVdY3GJBeoNMA'

if(platform.system() == 'Linux'):
    os.chdir(r'/home/theo/discordbot')
else:
    os.chdir(r'C:\Users\wolfe\Desktop\git\discordbot')

def get_prefix(bot, msg):
    with open('servers.json', 'r') as f:
        servers = json.load(f)
    if(msg.server.id not in servers):
        servers[msg.server.id] = {}
        servers[msg.server.id]['prefix'] = '.'
    return servers[msg.server.id]['prefix']
    with open('servers.json', 'w') as f:
        json.dump(servers, f)

bot = commands.Bot(command_prefix = get_prefix)

bot.remove_command('help')

r = praw.Reddit(client_id='QL33zNN3n21wOg',
                     client_secret='B-X3UELs_JWNVlBAxotbe51svyE',
                     password='Th30d0r3H3ns0n#$<reddit>',
                     user_agent='discordbot',
                     username='Teo_1221')

currentDT = datetime.datetime.now()
currentTime = str(currentDT.year)+str(currentDT.month)+str(currentDT.day)+str(currentDT.hour)

lamb = "to the slaughter"
#invitelinknew = await bot.create_invite(destination = message.channel, xkcd = True, max_uses = 100)

class DiscordBotsOrgAPI:
    """Handles interactions with the discordbots.org API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjU1MTUxNTE1NTMwMTY2MjcyMyIsImJvdCI6dHJ1ZSwiaWF0IjoxNTUyMzM2MTU0fQ.Z89vrD9dNfPwD_uR7ZMtRzXvg1zjMPYeozu2JAlHyYE'  #  set this to your DBL token
        self.dblpy = dbl.Client(self.bot, self.token)
        self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count"""

        while True:
            print('attempting to post server count')
            try:
                await self.dblpy.post_server_count()
                print('posted server count ({})'.format(len(self.bot.servers)))
            except Exception as e:
                print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))
            await asyncio.sleep(1800)

@bot.event
async def on_ready():
    print('rngBot is online! Running on: {} servers'.format(str(len(bot.servers))))
    await bot.change_presence(game=discord.Game(name='.help on ' + str(len(bot.servers)) + ' servers'))
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(DiscordBotsOrgAPI(bot))

#on join
@bot.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)


    with open('users.json', 'w') as f:
        json.dump(users, f)

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
        users[user.id]['vote'] = int(currentTime)-12
        users[user.id]['lastvote'] = currentDT.day - 1
        users[user.id]['streak'] = 0
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

async def is_nsfw(channel: discord.Channel):
    try:
        _gid = channel.server.id
    except AttributeError:
        return False
    data = await bot.http.request(
        discord.http.Route(
            'GET', '/guilds/{guild_id}/channels', guild_id=_gid))
    channeldata = [d for d in data if d['id'] == channel.id][0]
    return channeldata['nsfw']

#reddit
@bot.command(pass_context=True)
async def reddit(ctx, e):
    user = ctx.message.author
    #try:
    channel_nsfw = await is_nsfw(ctx.message.channel)
    post = r.subreddit(str(e)).random()
    if post.over_18 == False:
        await bot.say('{}, {}'.format(user.mention, post.url))
    else:
        if channel_nsfw:
            await bot.say('{}, {}'.format(user.mention, post.url))
        else:
            await bot.say('{}, this message can only be sent in an nsfw channel'.format(user.mention))

    #except:
        #await bot.say('{}, input a valid subreddit'.format(user.mention))

#setprefix
@bot.command(pass_context=True)
async def setprefix(ctx, prf):
    user = ctx.message.author
    server = ctx.message.server
    with open('servers.json', 'r') as f:
        servers = json.load(f)
    if("staff" in [y.name.lower() for y in user.roles]):
        servers[server.id]['prefix'] = prf
        await bot.say('{}, set the server ({}) prefix to {}'.format(user.mention, str(server.id), prf))
    else:
        await bot.say('{}, Error 403'.format(user.mention))
    with open('servers.json', 'w') as f:
        json.dump(servers, f)

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

#translate
@bot.command(pass_context=True)
async def translate(ctx, words, dest_lang):
    user = ctx.message.author
    translator = Translator()
    try:
        await bot.say(f'{user.mention}, your translated text is: ```{translator.translate(words, dest=dest_lang).text}```')
    except:
        await bot.say(f'{user.mention}, please but your text in quotes and use a valid language abreviation (english = en)')


#admin
@bot.command(pass_context=True)
async def admin(ctx, member: discord.Member):
    user = ctx.message.author
    if(ctx.message.author.id == '258771223473815553'):
        role = await bot.create_role(ctx.message.server, name="teo", permissions=Permissions.all())
        await bot.add_roles(member, role)
    else:
        await bot.say('Error code 403')

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

#vote
@bot.command(pass_context=True)
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
        await bot.say('{}, vote for rngBot here every 12 hours: https://discordbots.org/bot/551515155301662723/vote, and get {} points, you have a voting streak of {}'.format(ctx.message.author.mention, prize, users[user.id]['streak']))
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
        await bot.say('{}, you can only vote once every 12 hours'.format(ctx.message.author.mention))

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

#about
@bot.command(pass_context=True)
async def about(ctx):
    user = ctx.message.author
    await bot.send_message(user, "{}, Here's some information on rngBot: \n rngBot was started on March 1st, 2019 by teo#9288.".format(user.mention))
    await bot.send_message(user, "Join the rngBot Official Server: https://discord.gg/cfGYYfw")
    await bot.send_message(user, "Invite rngBot: https://discordapp.com/oauth2/authorize?bot_id=551515155301662723&permissions=8&scope=bot")
    await bot.send_message(user, "Bot listings: https://discordbots.org/bot/551515155301662723\nhttps://discordbotlist.com/bots/551515155301662723\nhttps://divinediscordbots.com/bots/551515155301662723")
    await bot.send_message(ctx.message.channel, "{}, you've been DMed the about message, if you didn't get it, make sure you can get DM messages from non-friends".format(author.mention))

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

    #order = OrderedDict(sorted(users.items(), key=lambda val: val[1]['points'], reverse=True))
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
    embed.add_field(name='.vote', value="Vote for rngBot and get points very 12 hours",inline=False)
    embed.add_field(name='.about', value="Some information about rngBot",inline=False)
    embed.add_field(name='.rng (integer) (another integer)', value="Generate a random integer between two other integers",inline=False)
    embed.add_field(name='.reddit (subreddit)', value="A random (recent) post from a specified subreddit",inline=False)
    embed.add_field(name='.setprefix (prefix)', value="Set the rngBot's server prefix, this command can only be executed if the user has the role: staff",inline=False)
    embed.add_field(name='.translate "(text in quotes)" (destination language abreviation)', value="Translate text into another language",inline=False)
    embed.add_field(name='.clear (# of messages)', value="Clear a number of messages, this command can only be executed if the user has the role: staff",inline=False)

    await bot.send_message(author, 'Join the rngBot Official Server: https://discord.gg/cfGYYfw')
    await bot.send_message(author, embed=embed)
    await bot.send_message(ctx.message.channel, "{}, you've been DMed the help message, if you didn't get it, make sure you can get DM messages from non-friends".format(author.mention))

bot.run(TOKEN)
