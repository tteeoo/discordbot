import json
import math
import os
import random
from decimal import Decimal

import discord
from discord.ext import tasks, commands

import dbl

file = open("../TOKEN.txt", "r")
TOKEN = str(file.read(59))
file = open("../DBL", "r")
API = str(file.read(155))
print(TOKEN)
print(API)
bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

token = API # set this to your DBL token
dblpy = dbl.DBLClient(bot, token, autopost=True) # Autopost will post your guild count every 30 minutes

async def on_guild_post():
    print("Server count posted successfully")

looptime = random.randint(15, 30)

with open('users.json', 'r') as f:
    users = json.load(f)
if int(round((users['The Casino']['points'] * 100) / 1000000000)) >=100:
    value = random.randint(1,5) * int(str(int(round((users['The Casino']['points'] * 100) / 1000000000)) - 99) + '00') + random.randint(1,100)
else:
    value = random.randint(1,5) * int(str(int(round((users['The Casino']['points'] * 100) / 1000000000)) - 101) + '00') + random.randint(1,100)

# loop
@tasks.loop(minutes=looptime)
async def timer():
    with open('users.json', 'r') as f:
        users = json.load(f)
    global value, looptime
    print('test')
    await bot.change_presence(status=discord.Status.online, activity=discord.Streaming(name='.help on ' + str(len(bot.guilds)) + ' servers', url='https://twitch.tv/#'))

    users['The Casino']['points'] += users['The Casino']['queue']
    users['The Casino']['queue'] = 0

    if int(round((users['The Casino']['points'] * 100) / 1000000000)) >=100:
        value = random.randint(1,5) * int(str(int(round((users['The Casino']['points'] * 100) / 1000000000)) - 99) + '00') + random.randint(1,100)
    else:
        value = random.randint(1,5) * int(str(int(round((users['The Casino']['points'] * 100) / 1000000000)) - 101) + '00') + random.randint(1,100)
    looptime = random.randint(15, 30)

# on start
@bot.event
async def on_ready():
    print('online')
    timer.start()
    await bot.change_presence(status=discord.Status.online, activity=discord.Streaming(name='.help on ' + str(len(bot.guilds)) + ' servers', url='https://twitch.tv/#'))

# on sent
@bot.event
async def on_message(message):
    # message logging
    print(
        f'message sent: {message.guild}: {message.channel}: {message.author}: {message.content}')

    # server json processing
    with open('servers.json', 'r') as f:
        servers = json.load(f)
    jsid = str(message.guild.id)
    if(jsid not in servers):
        servers[jsid] = {}

    # user json processing
    with open('users.json', 'r') as f:
        users = json.load(f)
    juid = str(message.author.id)
    if message.author.bot == False:
        try:
            if message.content[0] != '.':
                if juid in users:
                    if(users[juid]['points'] == 0):
                        users[juid]['points'] += 20
                        users[juid]['total'] += 20
                    else:
                        users[juid]['points'] += round(9 / users[juid]['points'] * 20 + 1)
                        users[juid]['total'] += round(9 / users[juid]['points'] * 20 + 1)

                    if(users['The Casino']['points'] == 0):
                        users['The Casino']['points'] += 20
                        users['The Casino']['total'] += 20
                    else:
                        users['The Casino']['points'] += round(9 / users[juid]['points'] * 20 + 1)
                        users['The Casino']['total'] += round(9 / users[juid]['points'] * 20 + 1)
            else:
                if juid not in users:
                    users[juid] = {}
                    users[juid]['points'] = 500
                    users[juid]['total'] = 500
                    users[juid]['stock'] = 0

                    users['The Casino']['points'] += 500
                    users['The Casino']['total'] += 500
                    await message.channel.send(f'{message.author.mention}, created new profile with 500 points')
        except IndexError:  # blank message
            ...
    # write json files
    with open('users.json', 'w') as f:
        json.dump(users, f)
    with open('servers.json', 'w') as f:
        json.dump(servers, f)

    # command processing
    await bot.process_commands(message)

# on delete
@bot.event
async def on_message_desentlete(message):
    print(
        f'message deleted: {message.guild}: {message.channel}: {message.author}: {message.content}')
# bal
@bot.command()
async def bal(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)

    juid = str(ctx.message.author.id)

    if juid in users:
        point = users[juid]['points']

        if int(point) > 999999999999999999999999999999:
            point = '{:.2e}'.format(Decimal(point))

        total = users[juid]['total']

        if int(total) > 999999999999999999999999999999:
            total = '{:.2e}'.format(Decimal(total))

        stock = users[juid]['stock']


        if int(stock) > 999999999999999999999999999999:
            stock = '{:.2e}'.format(Decimal(stock))

        await ctx.send(f'{ctx.message.author.mention}, you have {point} points, {total} total earnings, and {stock} stock')

# ping
@bot.command()
async def ping(ctx):
    await ctx.send(f'{ctx.message.author.mention}, {round(bot.latency, 3)} seconds')

# debug
@bot.command()
async def debug(ctx, arg):
    with open('users.json', 'r') as f:
        users = json.load(f)

    with open('servers.json', 'r') as f:
        servers = json.load(f)

    if(ctx.message.author.id == 258771223473815553):
        await ctx.send(eval(arg))
    else:
        await ctx.send(f'{ctx.message.author.mention}, unauthorized')

# rng
@bot.command()
async def rng(ctx, e, a):
    try:
        i = random.randint(int(e), int(a))
        await ctx.send(f'{ctx.message.author.mention}, {str(i)}')

    except:
        await ctx.send(f'{ctx.message.author.mention}, provide an integer, then another greater integer')

# give
@bot.command()
async def give(ctx, amount, use: discord.User):
    with open('users.json', 'r') as f:
        users = json.load(f)

    if(ctx.message.author.id == 258771223473815553):
        users[str(use.id)]['points'] += int(amount)
        await ctx.send(f'{ctx.message.author.mention}, gave {amount} points to {use.mention}')
    else:
        await ctx.send(f'{ctx.message.author.mention}, unauthorized')

    with open('users.json', 'w') as f:
        json.dump(users, f)

# pay
@bot.command()
async def pay(ctx, amnt, use: discord.User):
    with open('users.json', 'r') as f:
        users = json.load(f)

    juid = str(ctx.message.author.id)

    if amnt == 'half':
        amnt = round(users[juid]['points'] / 2)
    if amnt == 'all':
        amnt = users[juid]['points']

    if(int(amnt) <= 1000000):

        try:
            if(int(amnt) > 0):
                amnt = int(amnt)

                if(int(amnt) <= users[str(ctx.message.author.id)]['points']):
                    users[str(ctx.message.author.id)]['points'] -= int(amnt)
                    users[str(use.id)]['points'] += int(amnt)
                    users[str(use.id)]['total'] += int(amnt)

                    await ctx.send(f"{ctx.message.author.mention}, paid {use.mention} {amnt} points")

                else:
                    await ctx.send(f"{ctx.message.author.mention}, you don't have enough points to do that")
            else:
                await ctx.send(f"{ctx.message.author.mention}, you can only pay integers greater than 0")
        except Error:
            await ctx.send(f"{ctx.message.author.mention}, you can only pay integers greater than 0")

    else:
        await ctx.send(f"{ctx.message.author.mention}, there is a transaction limit of 1 million points")
    with open('users.json', 'w') as f:
        json.dump(users, f)

# stock
@bot.command()
async def stock(ctx, *args):
    with open('users.json', 'r') as f:
        users = json.load(f)
    global value
    juid = str(ctx.message.author.id)

    go = []

    tpoints = 0
    for key in users:
        tpoints += users[key]['points']
    print(args)

    try:
        for a in args:
            go.append(a)

        amnt = int(go[1])

        if go[0] == 'buy':
            if amnt > 0:
                if users[juid]['points'] >= value * amnt:
                    users[juid]['stock'] += amnt
                    users['The Casino']['queue'] += value * amnt
                    users['The Casino']['total'] += value * amnt
                    users[juid]['points'] -= value * amnt
                    await ctx.send(f"{ctx.message.author.mention}, bought {amnt} shares for {value} each")
                else:
                    await ctx.send(f"{ctx.message.author.mention}, you don't have enough points to do that")
            else:
                await ctx.send(f'{ctx.message.author.mention}, you can only buy a postive integer of stock')


        if go[0] == 'sell':
            if amnt > 0:
                if users[juid]['stock'] >= amnt:
                    users[juid]['stock'] -= amnt
                    users['The Casino']['queue'] -= value * amnt
                    users[juid]['total'] += value * amnt
                    users[juid]['points'] += value * amnt
                    await ctx.send(f"{ctx.message.author.mention}, sold {amnt} shares for {value} each")
                else:
                    await ctx.send(f"{ctx.message.author.mention}, you don't have enough shares to do that")
            else:
                await ctx.send(f'{ctx.message.author.mention}, you can only sell a postive integer of stock')

    except (IndexError, ValueError):
        await ctx.send(f'{ctx.message.author.mention}, one stock is currently worth {value} points, the casino has {users["The Casino"]["points"]} points')
    with open('users.json', 'w') as f:
        json.dump(users, f)


# lookup
@bot.command()
async def lookup(ctx, use: discord.User):
    with open('users.json', 'r') as f:
        users = json.load(f)
    try:
        point = users[str(use.id)]['points']
        if int(point) > 999999999999999999999999999999:
            point = "{:.2e}".format(Decimal(point))
        total = users[str(use.id)]['total']
        if int(total) > 999999999999999999999999999999:
            total = "{:.2e}".format(Decimal(total))
        stock = users[str(use.id)]['stock']
        if int(stock) > 999999999999999999999999999999:
            stock = "{:.2e}".format(Decimal(stock))

        await ctx.send(f'{ctx.message.author.mention}, {use.mention} has {point} points, {total} total earnings, and {stock} stock')

    except:
        await ctx.send(f'{ctx.message.author.mention}, {use.mention} does not have a profile')

# flip
@bot.command()
async def flip(ctx, amnt):
    with open('users.json', 'r') as f:
        users = json.load(f)

    juid = str(ctx.message.author.id)

    if amnt == 'all':
        amnt = users[juid]['points']

    if amnt == 'half':
        amnt = round(users[juid]['points'] / 2)

    try:
        amnt = int(amnt)
        if(int(amnt) > 0):

            e = random.randint(1, 2)
            j = random.randint(1, 128)
            if(int(amnt) <= users[juid]['points']):
                if amnt <= users['The Casino']['points']:
                    if(j == 1):
                        if(int(amnt) * int(amnt) > 999999999999999999999999999999):
                            winnings = str("{:.2e}".format(
                                Decimal(int(amnt) * int(amnt))))
                        else:
                            winnings = str(int(amnt) * 10)

                        users[juid]['points'] += int(amnt) * 10
                        users[juid]['total'] += int(amnt) * 10
                        users['The Casino']['points'] -= int(amnt) * 10
                        await ctx.send(f'{ctx.message.author.mention}, you hit the jackpot and won {winnings} points!')
                    else:
                        if(e == 1):
                            users[juid]['points'] += amnt
                            users[juid]['total'] += amnt
                            users['The Casino']['points'] -= amnt
                            await ctx.send(f'{ctx.message.author.mention}, you won {str(amnt)} points')
                        else:
                            users[juid]['points'] -= amnt
                            users['The Casino']['points'] += amnt
                            users['The Casino']['total'] += amnt
                            await ctx.send(f'{ctx.message.author.mention}, you lost {str(amnt)} points')
                else:
                    await ctx.send(f"{ctx.message.author.mention}, the casino doesn't have enough points")
            else:
                await ctx.send(f"{ctx.message.author.mention}, you don't have enough points to do that")
        else:
            await ctx.send(f'{ctx.message.author.mention}, you can only flip integers greater than 0')
    except ValueError:
        await ctx.send(f'{ctx.message.author.mention}, you can only flip integers greater than 0')

    with open('users.json', 'w') as f:
        json.dump(users, f)

# flip2
@bot.command()
async def flip2(ctx, amnt):
    with open('users.json', 'r') as f:
        users = json.load(f)

    juid = str(ctx.message.author.id)

    if amnt == 'all':
        amnt = users[juid]['points']

    if amnt == 'half':
        amnt = round(users[juid]['points'] / 2)

    try:
        if(int(amnt) > 0):
            amnt = int(amnt)
            e = random.randint(1, 10)
            j = random.randint(1, 128)
            if(int(amnt) <= users[juid]['points']):
                if amnt * amnt <= users['The Casino']['points']:
                    if(j == 1):
                        if(int(amnt) * int(amnt) * int(amnt) > 999999999999999999999999999999):
                            winnings = str("{:.2e}".format(
                                Decimal(int(amnt) * int(amnt) * 10)))
                        else:
                            winnings = str(int(amnt) * int(amnt) * 10)

                        users[juid]['points'] += int(amnt) * int(amnt) * 10
                        users[juid]['total'] += int(amnt) * int(amnt) * 10
                        users['The Casino']['points'] -= int(amnt) * int(amnt) * 10
                        await ctx.send(f'{ctx.message.author.mention}, you hit the jackpot and won {winnings} points!')
                    else:
                        if(int(amnt) * int(amnt) > 999999999999999999999999999999):
                            winnings = str("{:.2e}".format(
                                Decimal(int(amnt) * int(amnt))))
                        else:
                            winnings = str(int(amnt) * int(amnt))

                        if(e == 1):
                            users[juid]['points'] += int(amnt) * int(amnt)
                            users[juid]['total'] += int(amnt) * int(amnt)
                            users['The Casino']['points'] -= int(amnt) * int(amnt)
                            await ctx.send(f'{ctx.message.author.mention}, you won {winnings} points')
                        else:
                            if(int(amnt) * int(amnt) < users[juid]['points']):
                                users[juid]['points'] -= int(amnt) * int(amnt)
                                users['The Casino']['points'] += int(amnt) * int(amnt)
                                users['The Casino']['total'] += int(amnt) * int(amnt)
                                await ctx.send(f'{ctx.message.author.mention}, you lost {winnings} points')
                            else:
                                users['The Casino']['points'] += users[juid]['points']
                                users['The Casino']['total'] += users[juid]['points']
                                await ctx.send(f'{ctx.message.author.mention}, you lost {users[juid]["points"]} points')
                                users[juid]['points'] = 0
                else:
                    await ctx.send(f"{ctx.message.author.mention}, the casino doesn't have enough points")
            else:
                await ctx.send(f"{ctx.message.author.mention}, you don't have enough points to do that")
        else:
            await ctx.send(f"{ctx.message.author.mention}, you can only flip integers greater than 0")
    except ValueError:
        await ctx.send(f'{ctx.message.author.mention}, you can only flip integers greater than 0')

    with open('users.json', 'w') as f:
        json.dump(users, f)

# flip3
@bot.command()
async def flip3(ctx, amnt):
    with open('users.json', 'r') as f:
        users = json.load(f)

    juid = str(ctx.message.author.id)

    if amnt == 'all':
        amnt = users[juid]['points']

    if amnt == 'half':
        amnt = round(users[juid]['points'] / 2)

    try:
        amnt = int(amnt)
        if(int(amnt) > 0):
            e = random.randint(1, 4)
            j = random.randint(1, 128)

            if(int(amnt) <= users[juid]['points']):
                if amnt * amnt <= users['The Casino']['points']:
                    if(j == 1):
                        users[juid]['points'] += int(amnt) * 10
                        users[juid]['total'] += int(amnt) * 10
                        users['The Casino']['points'] -= int(amnt) * 10
                        await ctx.send(f'{ctx.message.author.mention}, you hit the jackpot and won {str(int(amnt) * 10)} points!')
                    else:
                        if(e == 4):
                            users[juid]['points'] -= int(amnt)
                            users['The Casino']['points'] += int(amnt)
                            users['The Casino']['total'] += int(amnt)
                            await ctx.send(f'{ctx.message.author.mention}, you lost {str(amnt)} points')
                        else:
                            users[juid]['points'] += round(int(amnt) / 3)
                            users[juid]['total'] += round(int(amnt) / 3)
                            users['The Casino']['points'] -= round(int(amnt) / 3)
                            await ctx.send(f'{ctx.message.author.mention}, you won {str(round(amnt / 3))} points')
                else:
                    await ctx.send(f"{ctx.message.author.mention}, the casino doesn't have enough points")
            else:
                await ctx.send(f"{ctx.message.author.mention}, you don't have enough points to do that")
        else:
            await ctx.send(f"{ctx.message.author.mention}, you can only flip integers greater than 0")
    except ValueError:
        await ctx.send(f"{ctx.message.author.mention}, you can only flip integers greater than 0")

    with open('users.json', 'w') as f:
        json.dump(users, f)

# top
@bot.command()
async def top(ctx):
    user = ctx.message.author
    with open('users.json', 'r') as f:
        users = json.load(f)
    del users['The Casino']
    order2 = sorted(
        users.items(), key=lambda val: val[1]['points'], reverse=True)
    firstp = str(order2[0])[2:]
    x = 0
    while(1 == 1):
        if (firstp[x] == "'"):
            break
        x += 1
    firstp = str(order2[0])[2:x + 2]
    firsts = users[firstp]['points']
    if int(firsts) > 999999999999999999999999999999:
        firsts = "{:.2e}".format(Decimal(firsts))

    secondp = str(order2[1])[2:]
    x = 0
    while(1 == 1):
        if (secondp[x] == "'"):
            break
        x += 1
    secondp = str(order2[1])[2:x + 2]
    seconds = users[secondp]['points']
    if int(seconds) > 999999999999999999999999999999:
        seconds = "{:.2e}".format(Decimal(seconds))

    thirdp = str(order2[2])[2:]
    x = 0
    while(1 == 1):
        if (thirdp[x] == "'"):
            break
        x += 1
    thirdp = str(order2[2])[2:x + 2]
    thirds = users[thirdp]['points']
    if int(thirds) > 999999999999999999999999999999:
        thirds = "{:.2e}".format(Decimal(thirds))

    fourthp = str(order2[3])[2:]
    x = 0
    while(1 == 1):
        if (fourthp[x] == "'"):
            break
        x += 1
    fourthp = str(order2[3])[2:x + 2]
    fourths = users[fourthp]['points']
    if int(fourths) > 999999999999999999999999999999:
        fourths = "{:.2e}".format(Decimal(fourths))

    fivep = str(order2[4])[2:]
    x = 0
    while(1 == 1):
        if (fivep[x] == "'"):
            break
        x += 1
    fivep = str(order2[4])[2:x + 2]
    fives = users[fivep]['points']
    if int(fives) > 999999999999999999999999999999:
        fives = "{:.2e}".format(Decimal(fives))

    firstp = bot.get_user(int(firstp))
    secondp = bot.get_user(int(secondp))
    thirdp = bot.get_user(int(thirdp))
    fourthp = bot.get_user(int(fourthp))
    fivep = bot.get_user(int(fivep))

    await ctx.send("{}, the top players are: \n \n {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points```".format(user.mention, firstp, firsts, secondp, seconds, thirdp, thirds, fourthp, fourths, fivep, fives))


# servertop
@bot.command()
async def servertop(ctx):
    user = ctx.message.author
    guild = ctx.message.guild
    with open('users.json', 'r') as f:
        users = json.load(f)
    del users['The Casino']
    q = 0
    guildMem = list()
    guildPoints = list()
    d = dict()
    for member in guild.members:
        if(str(member.id) in users):
            guildMem.append(str(member.id))
    for x in guildMem:
        guildPoints.append(users[x]['points'])
    while(int(q) < int(len(guildMem))):
        d.update({str(guildMem[q]): int(guildPoints[q])})
        q = q + 1
    order2 = sorted(d.items(), key=lambda val: val[1], reverse=True)
    firstp = str(order2[0])[2:]
    x = 0
    while(1 == 1):
        if (firstp[x] == "'"):
            break
        x += 1
    firstp = str(order2[0])[2:x + 2]
    firsts = users[firstp]['points']
    if int(firsts) > 999999999999999999999999999999:
        firsts = "{:.2e}".format(Decimal(firsts))

    secondp = str(order2[1])[2:]
    x = 0
    while(1 == 1):
        if (secondp[x] == "'"):
            break
        x += 1
    secondp = str(order2[1])[2:x + 2]
    seconds = users[secondp]['points']
    if int(seconds) > 999999999999999999999999999999:
        seconds = "{:.2e}".format(Decimal(seconds))

    if(len(order2) >= 3):
        thirdp = str(order2[2])[2:]
        x = 0
        while(1 == 1):
            if (thirdp[x] == "'"):
                break
            x += 1
        thirdp = str(order2[2])[2:x + 2]
        thirds = users[thirdp]['points']
        if int(thirds) > 999999999999999999999999999999:
            thirds = "{:.2e}".format(Decimal(thirds))

    if(len(order2) >= 4):
        fourthp = str(order2[3])[2:]
        x = 0
        while(1 == 1):
            if (fourthp[x] == "'"):
                break
            x += 1
        fourthp = str(order2[3])[2:x + 2]
        fourths = users[fourthp]['points']
        if int(fourths) > 999999999999999999999999999999:
            fourths = "{:.2e}".format(Decimal(fourths))

    if(len(order2) >= 5):
        fivep = str(order2[4])[2:]
        x = 0
        while(1 == 1):
            if (fivep[x] == "'"):
                break
            x += 1
        fivep = str(order2[4])[2:x + 2]
        fives = users[fivep]['points']
        if int(fives) > 999999999999999999999999999999:
            fives = "{:.2e}".format(Decimal(fives))

    if(len(order2) == 2):
        firstp = bot.get_user(int(firstp))
        secondp = bot.get_user(int(secondp))
        await ctx.send("{}, the top players on your server are: \n \n {} ```{} points``` {} ```{} points```".format(user.mention, firstp, firsts, secondp,  seconds))
    if(len(order2) == 3):
        firstp = bot.get_user(int(firstp))
        secondp = bot.get_user(int(secondp))
        thirdp = bot.get_user(int(thirdp))
        await ctx.send("{}, the top players on your server are: \n \n {} ```{} points``` {} ```{} points``` {} ```{} points```".format(user.mention, firstp, firsts, secondp,  seconds, thirdp, thirds))
    if(len(order2) == 4):
        firstp = bot.get_user(int(firstp))
        secondp = bot.get_user(int(secondp))
        thirdp = bot.get_user(int(thirdp))
        fourthp = bot.get_user(int(fourthp))
        await ctx.send("{}, the top players on your server are: \n \n {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points```".format(user.mention, firstp, firsts, secondp,  seconds, thirdp, thirds, fourthp, fourths))
    if(len(order2) >= 5):
        firstp = bot.get_user(int(firstp))
        secondp = bot.get_user(int(secondp))
        thirdp = bot.get_user(int(thirdp))
        fourthp = bot.get_user(int(fourthp))
        fivep = bot.get_user(int(fivep))
        await ctx.send("{}, the top players on your server are: \n \n {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points```".format(user.mention, firstp, firsts, secondp, seconds, thirdp, thirds, fourthp, fourths, fivep, fives))

# help
@bot.command()
async def help(ctx):
    await ctx.message.author.send("""****Isosceles is a server economy bot that gives points to users when they chat in servers, along with many other commands.****
`Users gain points, and then can gamble with points, as well as pay other users, and see leadboards
Points of course, are independent of the server and will transfer from server to server
The bot is currently in development and many more features are soon to come`
`Features in the works:
  - Server moderation
  - Reddit integration
  - And more! Suggestions are welcome on the discord server`
**For more info:**
  `- Discord Bot List:` https://top.gg/bot/650477168702259220
  `- Discord server:` https://discordapp.com/invite/TJjQmUp
  `- Invite the bot:` https://discordapp.com/api/oauth2/authorize?client_id=650477168702259220&permissions=8&scope=bot
  `- GitHub repo:` https://github.com/tteeoo/discordbot
***Commands***
**.bal**
  `- Shows your current balance`
**.ping**
  `- Checks isosceles' latency`
**.top**
  `- Displays the top 5 players`
**.servertop**
  `- Displays the top 5 players on the current server`
**.lookup (person)**
  `- Looks up a person's balance`
**.pay (amount/all/half) (person)**
  `- Pays a person an amount of points`
**.flip (amount/all/half)**
  `- 50% chance to win an amount of points, 50% chance to lose the amount of points`
**.flip2 (amount/all/half)**
  `- 10% chance to win an amount of points squared, 90% chance to lose the amount squared`
**.flip3 (amount/all/half)**
  `- 75% chance to win one third an amount of points, 25% chance to lose the amount`
 **.stock (buy/sell) (amount)**
   `- buy or sell an amount of stock, one stock is worth the average amount of points per user (.stock by itself for the value)`
 **.rng (integer) (greater integer)**
  `- Generates a random number between two numbers`
 **.help**
  `- Self explanatory`""")
    await ctx.send(f'{ctx.message.author.mention}, messaged you the help menu')

bot.run(TOKEN)
s.run()
