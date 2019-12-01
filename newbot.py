import json
import math
import os
import random
from decimal import Decimal

import discord
from discord.ext import commands

file = open("../TOKEN.txt", "r")
TOKEN = str(file.read(59))
print(TOKEN)

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

# on start
@bot.event
async def on_ready():
    print('online')
    await bot.change_presence(status=discord.Status.online, activity=discord.Streaming(name='.help on ' + str(len(bot.guilds)) + ' servers', url='https://www.twitch.tv/directory/all/tags/a59f1e4e-257b-4bd0-90c7-189c3efbf917?sort=VIEWER_COUNT'))

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
    try:
        if message.content[0] != '.':
            if juid in users:
                if(users[juid]['points'] == 0):
                    pnts = 20
                else:
                    pnts = round(2 / users[juid]['points'] * 20 + 1)
                await add_points(users, juid, pnts)
        else:
            if juid not in users:
                users[juid] = {}
                users[juid]['points'] = 500
                users[juid]['total'] = 500
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

# add points


async def add_points(users, juid, pnts):
    users[juid]['points'] += pnts
    users[juid]['total'] += pnts

    print(f'added {pnts} to {juid}')

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

        await ctx.send(f'{ctx.message.author.mention}, you have {point} points and {total} total earnings')

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

    if(ctx.message.author.id == 258771223473815553 or ctx.message.author.id == 546851070224105493):
        users[str(use.id)]['points'] += int(amount)
        users[str(use.id)]['total'] += int(amount)
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
    except ValueError:
        await ctx.send(f"{ctx.message.author.mention}, you can only pay integers greater than 0")

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

        await ctx.send(f'{ctx.message.author.mention}, {use.mention} has {point} points and {total} total earnings')

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

    try:
        amnt = int(amnt)
        if(int(amnt) > 0):

            e = random.randint(1, 2)

            if(int(amnt) <= users[juid]['points']):
                if(e == 1):
                    await add_points(users, juid, amnt)
                    await ctx.send(f'{ctx.message.author.mention}, you won {str(amnt)} points')
                else:
                    users[juid]['points'] -= int(amnt)
                    await ctx.send(f'{ctx.message.author.mention}, you lost {str(amnt)} points')
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

    try:
        if(int(amnt) > 0):
            amnt = int(amnt)
            e = random.randint(1, 10)
            if(int(amnt) * int(amnt) > 999999999999999999999999999999):
                winnings = str("{:.2e}".format(Decimal(int(amnt) * int(amnt))))
            else:
                winnings = str(int(amnt) * int(amnt))
            if(int(amnt) <= users[juid]['points']):
                if(e == 1):
                    users[juid]['points'] += int(amnt) * int(amnt)
                    users[juid]['total'] += int(amnt) * int(amnt)
                    await ctx.send(f'{ctx.message.author.mention}, you won {winnings} points')
                else:
                    if(int(amnt) * int(amnt) < users[juid]['points']):
                        users[juid]['points'] -= int(amnt) * int(amnt)
                        await ctx.send(f'{ctx.message.author.mention}, you lost {winnings} points')
                    else:
                        users[juid]['points'] = 0
                        await ctx.send(f'{ctx.message.author.mention}, you lost {winnings} points')
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

    try:
        amnt = int(amnt)
        if(int(amnt) > 0):
            e = random.randint(1, 4)

            if(int(amnt) <= users[juid]['points']):
                if(e == 1):
                    users[juid]['points'] += round(int(amnt) / 3)
                    users[juid]['total'] += round(int(amnt) / 3)
                    await ctx.send(f'{ctx.message.author.mention}, you won {str(round(amnt / 3))} points')
                if(e == 2):
                    users[juid]['points'] += round(int(amnt) / 3)
                    users[juid]['total'] += round(int(amnt) / 3)
                    await ctx.send(f'{ctx.message.author.mention}, you won {str(round(amnt / 3))} points')
                if(e == 3):
                    users[juid]['points'] += round(int(amnt) / 3)
                    users[juid]['total'] += round(int(amnt) / 3)
                    await ctx.send(f'{ctx.message.author.mention}, you won {str(round(amnt / 3))} points')
                if(e == 4):
                    users[juid]['points'] -= int(amnt)
                    await ctx.send(f'{ctx.message.author.mention}, you lost {str(amnt)} points')
            else:
                await ctx.send(f"{ctx.message.author.mention}, you don't have enough points to do that")
        else:
            await ctx.send(f"{ctx.message.author.mention}, you can only flip integers greater than 0")
    except ValueError:
        await ctx.send(f"{ctx.message.author.mention}, you can only flip integers greater than 0")

    with open('users.json', 'w') as f:
        json.dump(users, f)


# VIEWER DISCRETION IS ADVISED
# The following two functions are possibly the messiest I have every written
# If you know python, do not read them. They will pain you
# I wrote the m a long time ago and have not changed them because... They work. I'm afraid if I try to, they will break

# top
@bot.command()
async def top(ctx):
    user = ctx.message.author
    with open('users.json', 'r') as f:
        users = json.load(f)

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

    await ctx.send("{}, the top players are: \n \n {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points```".format(user.mention, '<@' + firstp + '>', firsts, '<@' + secondp + '>',  seconds, '<@' + thirdp + '>', thirds, '<@' + fourthp + '>', fourths, '<@' + fivep + '>', fives))


# servertop
@bot.command()
async def servertop(ctx):
    user = ctx.message.author
    guild = ctx.message.guild
    with open('users.json', 'r') as f:
        users = json.load(f)
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
        await ctx.send("{}, the top players on your server are: \n \n {} ```{} points``` {} ```{} points```".format(user.mention, '<@' + firstp + '>', firsts, '<@' + secondp + '>',  seconds))
    if(len(order2) == 3):
        await ctx.send("{}, the top players on your server are: \n \n {} ```{} points``` {} ```{} points``` {} ```{} points```".format(user.mention, '<@' + firstp + '>', firsts, '<@' + secondp + '>',  seconds, '<@' + thirdp + '>', thirds))
    if(len(order2) == 4):
        await ctx.send("{}, the top players on your server are: \n \n {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points```".format(user.mention, '<@' + firstp + '>', firsts, '<@' + secondp + '>',  seconds, '<@' + thirdp + '>', thirds, '<@' + fourthp + '>', fourths))
    if(len(order2) >= 5):
        await ctx.send("{}, the top players on your server are: \n \n {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points``` {} ```{} points```".format(user.mention, '<@' + firstp + '>', firsts, '<@' + secondp + '>',  seconds, '<@' + thirdp + '>', thirds, '<@' + fourthp + '>', fourths, '<@' + fivep + '>', fives))

# help
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        colour=discord.Colour.purple()
    )

    embed.set_author(name='isosceles commands')
    embed.add_field(
        name='.bal', value="shows your current balance", inline=False)
    embed.add_field(
        name='.ping', value="checks isosceles' latency", inline=False)
    embed.add_field(
        name='.top', value="displays the top 5 players", inline=False)
    embed.add_field(
        name='.servertop', value="displays the top 5 players on the current server", inline=False)
    embed.add_field(name='.lookup (person)',
                    value="looks up a different person's balance", inline=False)
    embed.add_field(name='.pay (amount) (person)',
                    value='pays a person an amount of points', inline=False)
    embed.add_field(name='.flip (amount)',
                    value='50% chance to win an amount of points, 50% chance to lose the amount of points', inline=False)
    embed.add_field(name='.flip2 (amount)',
                    value='10% chance to win an amount of points squared, 90% chance to lose the amount squared', inline=False)
    embed.add_field(name='.flip3 (amount)',
                    value='75% chance to win one third an amount of points, 25% chance to lose the amount', inline=False)
    embed.add_field(name='.rng (integer) (greater integer)',
                    value="generates a random number between two numbers", inline=False)
    await ctx.send(embed=embed)

bot.run(TOKEN)
