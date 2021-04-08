import discord
import os
import requests
from bs4 import BeautifulSoup
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
  
  if message.content.startswith('!monster'):
      material_command = message.content.strip().split(' ', 1)
      await message.channel.send(monster_finder(material_command[1]))

def material_finder(material):
  website = 'https://monsterhunterrise.wiki.fextralife.com/'
  material_edited = material
  if '+' in material:
    material_edited = material + '+'
  material_link = material_edited.replace(' ', '+')
  full_website = website + material_link
  r = requests.get(full_website)
  print(r.status_code)
  if r.status_code == 404:
    return f'No material named "{material}", did you spell it correctly?'
  return full_website

def monster_finder(monster):
  page = requests.get('https://game8.co/games/Monster-Hunter-Rise/archives/316137')
  soup = BeautifulSoup(page.content, 'html.parser')
  for link in soup.find_all("a", {"class": "a-link"}):
    if link.text.lower() == monster.lower():
      return link['href']
  return f'No small monster named "{monster}", did you spell it correctly?'

def about():
  return "A dedicated Discord bot for Hoontas :crossed_swords:"

def help():
  return 'Commands:\n**!hoonta about** -- bot description\n**!material [name of material]** -- shows what monster drops the desired material or where to find it\n**!monster [name of monster]** -- shows map location to find small monsters'

client.run(os.getenv('TOKEN'))