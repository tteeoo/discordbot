# isosceles discord bot

**Some of the bot's code is very messy, as I wrote some of the functions a long time ago, but they work.**

## Isosceles is a server economy bot that gives points to users when they chat in servers, along with many other commands.

Users gain points, and then can gamble with points, as well as pay other users, and see leadboards

Points of course, are independent of the server and will transfer from server to server

The bot is currently in development and many more features are soon to come

Anyone is free to fork, reproduce, or pull the code; This bot may serve as a template for bots of its nature

Pardon the lazy commit messages, whenever it says "ran" I am transfering from the server to my development computer, then I implement the update and push it back to the server with the message for the update.

**Features in the works:**

  - Bug squashing
  - Server moderation
  - Reddit integration
  - And more! Suggestions are welcome on the discord server

**For more info:**

  - Discord Bot List: https://top.gg/bot/650477168702259220
  - Discord server: https://discordapp.com/invite/TJjQmUp

# <a href="https://discordapp.com/api/oauth2/authorize?client_id=650477168702259220&permissions=8&scope=bot">Invite the bot</a> 

<hr>

# Run without docker  
create .env file and add this to it.
```
TOKEN=your token here
```
Then run bot.py

# Deploy using docker? [DockerHub](https://hub.docker.com/r/cool2zap/isosceles-bot) 
```sh
docker run -d -e TOKEN="your token" cool2zap/isosceles-bot
```

# Commands

**.bal**

  - Shows your current balance
  
**.ping**

  - Checks isosceles' latency
 
**.top**

  - Displays the top 5 players
  
**.servertop**

  - Displays the top 5 players on the current server
  
**.lookup (person)**

  - Looks up a person's balance
  
**.pay (amount/all/half) (person)**

  - Pays a person an amount of points
  
**.flip (amount/all/half)**

  - 50% chance to win an amount of points, 50% chance to lose the amount of points
  
**.flip2 (amount/all/half)**

  - 10% chance to win an amount of points squared, 90% chance to lose the amount squared
  
**.flip3 (amount/all/half)**

  - 75% chance to win one third an amount of points, 25% chance to lose the amount
  
 **.rng (integer) (greater integer)**

  - Generates a random number between two numbers
  
 **.coin (buy/sell) (amount/(all/half for sell)/(max for buy))**

  - coin is another currency besides points; the value is equal to the average points per user; it is bought and sold for its point value
  
 **.help**

  - Self explanatory
