import os
import time
import discord
from discord.ext import commands
from random import randint
import sqlite3
import idk

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS user_data (
    user_id TEXT PRIMARY KEY,
     cash INTEGER,
    multiplier INTEGER
)''')

user_cash = {}
user_multiplier = {}
set_cash_authorized = [595682667349934109, 697494341664636959]

cursor.execute('SELECT user_id, cash, multiplier FROM user_data')
for row in cursor.fetchall():
  user_id, cash, multiplier = row
  user_cash[user_id] = cash
  user_multiplier[user_id] = multiplier

conn.close()

def update_user_data(user_id, cash, multiplier):
  conn = sqlite3.connect('user_data.db')
  cursor = conn.cursor()

  cursor.execute('INSERT OR REPLACE INTO user_data (user_id, cash, multiplier) VALUES (?, ?, ?)', (user_id, cash, multiplier))
  conn.commit()
  conn.close()

@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name}')

@bot.command(brief='!count [n]', description='Counts from 1 to [n]')
async def count(ctx, n: int):
  for i in range (n):
    await ctx.send(i+1)
    time.sleep (0.5)

@bot.command(brief='!countrange [x] [y]', description='Counts from [x] to [y]')
async def countrange(ctx, ns: int, ne: int):
  if ns > ne:
    await ctx.send('Start must be less than or equal to end')
  else:
    for i in range (ne-ns+1):
      await ctx.send(ns+i)
      time.sleep (0.5)

@bot.command(brief='!abc [end_letter]', description='Says the alphabet from a to [end_letter]')
async def abc(ctx, a: str):
  a = a.lower()
  alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
  i = 0
  x = 0
  letter = ""
  for letters in (alphabet):
    if a == letters:
      x = x + 1
  if x == 0:
    await ctx.send(a + " is not a single letter in the alphabet")
  else:
    while letter != a:
      letter = alphabet[i]
      i = i + 1
      await ctx.send(letter)
      time.sleep (0.5)

@bot.command(brief='!repeat [x] [n]', description='[x] is repeated [n] times')
async def repeat (ctx, b: str, amount: int):
  if "@" in b:
    await ctx.send ("You cannot spam ping someone (or have the character: @, in your message.)")
  else:
    for i in range (amount):
      await ctx.send (b)
      time.sleep (0.5)

@bot.command()
async def set_cash(ctx, value):
  user_id = str(ctx.author.id)
  value = idk.abbreviate (value)
  x = 0
  if int (value) > 100000000000000000000000000000:
    await ctx.send (f'{ctx.author.mention}, you can not set cash to that high of a number.')
    return
  if user_id not in user_multiplier:
    user_multiplier[user_id] = 1
  for id in set_cash_authorized:
    if int(user_id) == id:
      user_cash[user_id] = value
      await ctx.send("Information updated.")
      update_user_data (user_id, user_cash[user_id], user_multiplier[user_id])
      x = x + 1
  if x == 0:
    await ctx.send ("You are not authorized to use this command.")

@bot.command(brief='!cash', description='Tells user how much cash they have (rounded).')
async def cash(ctx):
  user_id = str(ctx.author.id)

  if user_id in user_cash:
    value = user_cash[user_id]
  else:
    value = 1000
    user_cash[user_id] = value
  await ctx.send(f"{ctx.author.mention}, your cash is {idk.compact (value)}.")

@bot.command(brief='!cash_exact', description='Tells user exactly how much cash they have.')
async def cash_exact (ctx):
  user_id = str(ctx.author.id)

  if user_id in user_cash:
    value = user_cash[user_id]
  else:
    value = 1000
    user_cash[user_id] = value
  await ctx.send(f"{ctx.author.mention}, your cash is {value}.")

@bot.command(brief='!gamble [amount]', description='Gambles [amount] cash')
async def gamble (ctx, amount):
  user_id = str(ctx.author.id)

  amount = idk.abbreviate (amount)
  if user_id not in user_cash:
    user_cash[user_id] = 1000
  if user_id not in user_multiplier:
    user_multiplier[user_id] = 1
  value = user_cash[user_id]
  if int (value) < int (amount):
    await ctx.send ("Insufficient cash")
  else:
    rng = randint (1, 20)
    if rng == 1:
      await ctx.send (f"{ctx.author.mention}, you gambled {idk.compact (amount)} cash and won {idk.compact(25 * int(idk.abbreviate(str(amount))))} cash.")
      user_cash[user_id] = int (value) + int (amount) * 25
      update_user_data (user_id, user_cash[user_id], user_multiplier[user_id])
    else:
      await ctx.send (f"{ctx.author.mention}, you gambled {idk.compact (amount)} cash and lost {idk.compact (amount)} cash.")
      user_cash[user_id] = int (value) - int (amount)
      update_user_data (user_id, user_cash[user_id], user_multiplier[user_id])

@bot.command(brief='!lottery [num_tickets]', description='Buys [num_tickets] tickets for the lottery for 50 cash each.')
async def lottery (ctx, tickets):
  user_id = str(ctx.author.id)
  tickets = idk.abbreviate (tickets)
  cost = int (tickets) * 50
  if (user_id not in user_cash):
    user_cash[user_id] = 1000
  if user_id not in user_multiplier:
    user_multiplier[user_id] = 1
  if (int(user_cash[user_id]) < cost):
    await ctx.send (f"{ctx.author.mention} You cannot afford {tickets} tickets.")
  else:
    user_cash[user_id] = int (user_cash[user_id]) - cost
    win = False
    for i in range (int(tickets)):
      rng = randint (1, 100000)
      if rng == 1:
        win = True
        break
    if win:
      user_cash[user_id] = int (user_cash[user_id]) + 10000000
      await ctx.send (f"{ctx.author.mention} You won 10 million cash from the lottery!")
      update_user_data (user_id, user_cash[user_id], user_multiplier[user_id])
    else:
      await ctx.send (f"{ctx.author.mention} You did not win anything from the lottery.")

@bot.command(brief='!work', description='User makes money by working')
async def work (ctx):
  user_id = str(ctx.author.id)
  if user_id not in user_cash:
    user_cash[user_id] = 1000
  if user_id not in user_multiplier:
    user_multiplier[user_id] = 1
  rng_Pay = randint(1,10) * randint(1, 10) * randint(1, 10) * randint (1, 10) * int(user_multiplier[user_id])
  user_cash[user_id] = int (user_cash[user_id]) + rng_Pay
  await ctx.send (f"{ctx.author.mention}, you worked and earned {idk.compact (rng_Pay)} cash.")
  update_user_data (user_id, user_cash[user_id], user_multiplier[user_id])

@bot.command(brief='!check_cash [id] [username]', description='Says the amount of cash the user with the id [id] has.')
async def check_cash (ctx, id, name):
  if id not in user_cash:
    user_cash[id] = 1000
  value = user_cash[id]
  await ctx.send (f"{name} has {idk.compact (value)} cash.")

@bot.command(brief='!shop', description='Tells user the items they can buy from the shop.')
async def shop (ctx):
  await ctx.send (f"{ctx.author.mention}\n\nWelcome to the shop! Here are the items you can buy:\n1. Worker Potion - 10k cash\n2. Mega Worker Potion - 1m cash\n3. Giga Worker Potion - 100m cash\n4. Ultra Worker Potion - 10b cash\n5. Worker Emperor Potion - 1t cash\n\n\nEnter !buy [number] to buy item.")

@bot.command(brief='!buy [item_num] [amount]', description='Buys [amount] of the item from the shop.')
async def buy (ctx, item: int, number):
  user_id = str (ctx.author.id)

  number = idk.abbreviate (number)
  amount = int (number)
  if user_id not in user_cash:
    user_cash[user_id] = 1000
  if user_id not in user_multiplier:
    user_multiplier[user_id] = 1
  if user_id not in user_cash:
    user_cash[user_id] = 1000
  if item == 1:
    if int(user_cash[user_id]) >= 10000 * amount:
      user_cash[user_id] = int (user_cash[user_id]) - (10000 * amount)
      user_multiplier[user_id] = int (user_multiplier[user_id]) + (1 * amount)
      await ctx.send (f"{ctx.author.mention}, you bought {amount} worker potion for {idk.compact (amount * 10000)}.")
    else:
      await ctx.send (f"{ctx.author.mention}, you cannot afford {amount} worker potion.")
  elif item == 2:
    if int(user_cash[user_id]) >= 1000000 * amount:
      user_cash[user_id] = int (user_cash[user_id]) - 1000000 * amount
      user_multiplier[user_id] = int (user_multiplier[user_id]) + 200 * amount
      await ctx.send (f"{ctx.author.mention}, you bought {idk.compact(amount)} mega worker potion for {idk.compact (amount * 1000000)} cash.")
    else:
      await ctx.send (f"{ctx.author.mention}, you cannot afford {idk.compact(amount)} mega worker potion.")
  elif item == 3:
    if int(user_cash[user_id]) >= 100000000 * amount:
      user_cash[user_id] = int (user_cash[user_id]) - 100000000 * amount
      user_multiplier[user_id] = int (user_multiplier[user_id]) + 40000 * amount
      await ctx.send (f"{ctx.author.mention}, you bought {idk.compact(amount)} giga worker potion for {idk.compact (amount * 100000000)} cash.")
    else:
      await ctx.send (f"{ctx.author.mention}, you cannot afford {idk.compact(amount)} giga worker potion.")
  elif item == 4:
    if int(user_cash[user_id]) >= 10000000000 * amount:
      user_cash[user_id] = int (user_cash[user_id]) - 10000000000 * amount
      user_multiplier[user_id] = int (user_multiplier[user_id]) + 8000000 * amount
      await ctx.send (f"{ctx.author.mention}, you bought {idk.compact(amount)} ultra worker potion for {idk.compact (amount * 10000000000)} cash.")
    else:
      await ctx.send (f"{ctx.author.mention}, you cannot afford {idk.compact(amount)} ultra worker potion.")
  elif item == 5:
    if int(user_cash[user_id]) >= 1000000000000 * amount:
      user_cash[user_id] = int (user_cash[user_id]) - 1000000000000 * amount
      user_multiplier[user_id] = int (user_multiplier[user_id]) + 16000000000 * amount
      await ctx.send (f"{ctx.author.mention}, you bought {idk.compact(amount)} worker emperor potion for {idk.compact (amount * 1000000000000)} cash.")
    else:
      await ctx.send (f"{ctx.author.mention}, you cannot afford {idk.compact(amount)} worker emperor potion.")
  else:
    await ctx.send (f"{ctx.author.mention}, that is an invalid choice.")
  if int(user_multiplier[user_id]) >= 100000000000000000000:
    await ctx.send (f"{ctx.author.mention}, you have reached the maximum multiplier.")
    user_multiplier[user_id] = 100000000000000000000
  update_user_data (user_id, user_cash[user_id], user_multiplier[user_id])

@bot.command(brief='!multiplier', description='Tells user how much their work multiplier is (rounded).')
async def multiplier (ctx):
  user_id = str (ctx.author.id)
  if user_id not in user_multiplier:
    user_multiplier[user_id] = 1
  await ctx.send (f"{ctx.author.mention}, your work multiplier is {idk.compact(user_multiplier[user_id])}.")

@bot.command(brief='!mult_exact', description='Tells user exactly how much their work multiplier is.')
async def mult_exact (ctx):
  user_id = str (ctx.author.id)
  if user_id not in user_multiplier:
    user_multiplier[user_id] = 1
  await ctx.send (f"{ctx.author.mention}, your work multiplier is {user_multiplier[user_id]}.")

@bot.command()
async def change_cash(ctx, id, value):
  user_id = str(ctx.author.id)
  value = idk.abbreviate (value)
  x = 0
  if int (value) > 100000000000000000000000000000:
    await ctx.send (f'{ctx.author.mention}, you can not set cash to that high of a number.')
    return
  if str(id) not in user_multiplier:
    user_multiplier[str(id)] = 1
  for ids in set_cash_authorized:
    if int(id) == ids:
      user_cash[str(id)] = value
      await ctx.send("Information updated.")
      update_user_data (str(id), user_cash[str(id)], user_multiplier[str(id)])
      x = x + 1
  if x == 0:
    await ctx.send ("You are not authorized to use this command.")

bot.run(os.environ['TOKEN'])