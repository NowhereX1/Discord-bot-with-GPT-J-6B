import discord.ext
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
from dhooks import Embed
from deep_translator import GoogleTranslator
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r"tesseract_path"
from PIL import Image
import shutil
import requests
import os
import gpt_api

client = discord.Client()
guild = discord.Guild

parameters = {
    'max_new_tokens':200,#150
    'temperature': 0.5, #09
    'end_sequence': "###",
    'do_sample': True,
    'top_p': 0.75,#07
    'top_k': 100,
    'no_repeat_ngram_size': 3,
    'max_length': 200,
    'best_of': 1
}
            

@client.event
async def on_ready():
    print('{0.user} is online'.format(client))
    await client.change_presence(activity=discord.Game('! Hello World | active on ' + str(len(client.guilds)) + " servers"))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!"):

        try:
            url = message.attachments[0].url            
        except IndexError:

            data = message.content
            redata = data.replace("!"," ")
            en = GoogleTranslator(source="auto", target="en").translate(redata)
            response = gpt_api.query(en,parameters)
            await message.channel.send(response,reference=message)

        else:
            if url[0:26] == "https://cdn.discordapp.com":   
                r = requests.get(url, stream=True)
                imageName = 'image.png'
                with open(imageName, 'wb') as out_file:
                    print('Saving image: ' + imageName)
                    shutil.copyfileobj(r.raw, out_file)
                
                img = Image.open("image.png")
                text = tess.image_to_string(img)
                responseText = gpt_api.query(text,parameters)
                await message.channel.send(responseText,reference=message)
                os.remove("image.png")
                print("Removing Image")

client.run("TOKEN_HERE")
