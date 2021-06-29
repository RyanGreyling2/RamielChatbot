import discord
import os
import time
from parse import Result, parse
from datetime import date

from dbhelper import *

from dotenv import load_dotenv
load_dotenv('./.env')

client = discord.Client()

async def handleLogout():
    await client.close()



@client.event
async def on_ready():  
    # Load Alias Table
    await load_alias()

    print('We have logged in as {0.user}'.format(client))



@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.mentions:
        subject = message.mentions[0]
        if subject.name == "Ramiel" and subject.bot == True:
            name = message.author.name
            discrim = message.author.discriminator
            author = message.author
            try: author = await get_alias(author.name, author.discriminator)
            except KeyError: pass
            await message.channel.send("Hello {0}! Use *help to see a list of available commands".format(author))
        return
    
    if message.content.startswith('*help'):
        help_docs = open('help.txt', 'r')
        out_message = ""
        for line in help_docs:
            out_message += line
        help_docs.close()
        await message.channel.send(out_message)
        return


    if message.content.startswith('*measure'):
        await message.channel.send("Ramiel's measurements: 6 Vertices, 12 Edges, and 8 Faces")
        return

    if message.content.startswith('*spoiler'):
        await message.channel.send("Shinji touches someone")
        return

    if message.content.startswith('*stop'):
        name = message.author.name
        discrim = message.author.discriminator
        if name == os.environ['AUTHOR_NAME'] and discrim == os.environ['AUTHOR_DISCRIM']:
            if 'force' in message.content:
                print("FORCED SHUTDOWN BY RYAN")
                await client.close()
                return
            print("Shutdown by Ryan")
            await handleLogout()
            return
        else:
            try: 
                alias = await get_alias(name, discrim)
                if alias == 'Hans':
                    await message.channel.send(file=discord.File('./images/Asuka.jpg'))
                    return
            except KeyError: pass
        
                
        for role in message.author.roles:
                if role.name == 'THE FIRST PILGRIMS':
                    print("Ramiel shut down by the First Pilgrim {0.author}".format(message))
                    await handleLogout()
        return
    

    if message.content.startswith('*wordcloud'):
        if message.author.name == os.environ['AUTHOR_NAME'] and message.author.discriminator == os.environ['AUTHOR_DISCRIM']:
            text_channel_list = []
            for guild in client.guilds:
                for channel in guild.text_channels:
                    text_channel_list.append(channel)

            def correctChannel(text_channel):
                if text_channel.name == 'general' or text_channel.name == 'oldgeneral':
                    return True
                else:
                    return False
            
            text_channel_list = filter(correctChannel, text_channel_list)

            dump_file = open('dump.txt', 'w', encoding='utf-8')
            for text_channel in text_channel_list:
                async for msg in text_channel.history(limit=10000):
                    if msg.author.name == 'PLACEHOLDER' and 'http' not in msg.content:
                        print(msg.content)
                        dump_file.write(msg.content)
            
            dump_file.close()
            print("The file dump is complete")


    if message.content.startswith('*test'): # Secret command. Should not be in docs
        if message.author.name == os.environ['AUTHOR_NAME'] and message.author.discriminator == os.environ['AUTHOR_DISCRIM']:
            alias = 'Ryan'
            result = parse("*test{}", message.content)
            if message.content == '⛸️⛸️':
                print("Ice Equal")
            if result[0] == '⛸️⛸️':
                print("Parse Equal")
            print(message.content)
            print('⛸️⛸️')
        return
    
    if message.content.startswith('*date'):
        today = date.today()
        d1 = today.strftime("Today's date is %B %d, 1984")
        await message.channel.send(d1)
        return

client.run(os.environ['TOKEN'])