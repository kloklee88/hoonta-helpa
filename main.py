import discord
import os
import requests
from keep_alive import keep_alive

#Flask Server to keep repl.it alive
keep_alive()

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
      return

  #Process message commands
  full_command = message.content.strip().split(' ')
  if message.content.startswith('!hoonta'):
    print(full_command)
    if len(full_command) == 2:
      first_command = full_command[1]
      if first_command == 'about':
        await message.channel.send(about())
      elif first_command == 'help':
        await message.channel.send(help())
    else:
      await message.channel.send(help())
  
  if message.content.startswith('!material'):
      material_command = message.content.strip().split(' ', 1)
      await message.channel.send(material_finder(material_command[1]))

def material_finder(material):
  website = 'https://monsterhunterrise.wiki.fextralife.com/'
  if '+' in material:
    material = material + '+'
  material_link = material.replace(' ', '+')
  full_website = website + material_link
  r = requests.get(full_website)
  print(r.status_code)
  if r.status_code == 404:
    return f'No material named "{material}", did you spell it correctly?'
  return full_website

def about():
  return "A dedicated Discord bot for Hoontas :crossed_swords:"

def help():
  return 'Commands:\n**!hoonta about** -- bot description\n**!material [name of material]** -- shows what monster drops the desired material or where to find it'

client.run(os.getenv('TOKEN'))