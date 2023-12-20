import discord
import requests
import json
import random
from replit import db

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]

starter_encouragements = [
"Cheer up!", 
"Hang in there!",
"You got this!",
"I know it's tough, but you're tougher!",
"Don't stress. Be strong!",
"Sending some good vibes and happy thoughts your way",
"If you ever need to talk, or just cry, you know where to find me!",
"Dont worry because the next chapter of your life is going to be so amazing!"]

def get_joke():
  respond = requests.get('https://api.chucknorris.io/jokes/random')
  json_info = json.loads(respond.text)
  joke = json_info['value']
  return(joke)


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " ~" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  
  else:
    db["encouragements"] = [encouraging_message]
  

@client.event

async def on_read():
  print('We have logged in as   {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  
  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if message.content.startswith('$joke'):
    joke = get_joke()
    await message.channel.send(joke)

  if message.content.startswith('hello'):
    await message.channel.send('Hello! How are you doing?')
    
  if message.content.startswith('howdy'):
    await message.channel.send('Pleased to meet you')

  if message.content.startswith('hi'):
    await message.channel.send('How’s it going?')


  options = starter_encouragements
  if "encouragements" in db.keys():
    options = options + list(db["encouragements"])

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added")

  
client.run('OTQ3NzE0MjQxMjQ1MzgwNjM4.YhxRqg.pXrJs6vbOY3ONuEM_SkwuMKDJ9g')
