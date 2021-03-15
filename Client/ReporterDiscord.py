import os
import discord
import io
import aiohttp
from dotenv import load_dotenv
import asyncio
from threading import Thread


# python DiscordSA.py --ip 192.168.56.1 --port 8000


class ReporterDiscord:
    def __init__(self, ip, port):

        load_dotenv()
        self.TOKEN = os.getenv('DISCORD_TOKEN')
        self.GUILD = os.getenv('DISCORD_GUILD')

        print("Token:", self.TOKEN)
        print("Guild:", self.GUILD)

        self.client = discord.Client()

        serverLocation = "http://" + ip + ":" + port

        print("Server location: " + serverLocation)

        @self.client.event
        async def on_ready():
            for guild in self.client.guilds:
                if guild.name == self.GUILD:
                    print("Equal!")
                    break
            print(
                f'{self.client.user} is connected to the following guild:\n'
                f'{guild.name}(id: {guild.id})'
            )


        # @self.client.event
        # async def on_message(message):
        #     channel = self.client.get_channel(797955245665157152)
        #     if message.author == self.client.user:
        #         return

        #     # User asked for count
        #     if message.content == '!count':
        #         response = "I found this many boxes!"
        #         channel = self.client.get_channel(797955245665157152)
        #         await channel.send(response)

        #     # User asked for screenshot
        #     if message.content == "!image":
        #         async with aiohttp.ClientSession() as session:
        #             # Request image
        #             async with session.get(serverLocation + "/single.jpg") as resp:

        #                 # No image found!
        #                 if resp.status != 200:
        #                     return await channel.send('Could not download file...')

        #                 # Read response and send data to channel
        #                 data = io.BytesIO(await resp.read())
        #                 await channel.send(file=discord.File(data, 'screenshot.jpg'))

        #     # User asked for boxes
        #     if message.content == '!boxes':
        #         async with aiohttp.ClientSession() as session:
        #             async with session.get(serverLocation + "/boxes") as resp:

        #                 # Nothing found
        #                 if resp.status != 200:
        #                     return await channel.send('Could not download file...')

        #                 # "utf-8" part removes b'<data>' and automatically formats
        #                 data = str(await resp.read(), "utf-8")
        #                 channel = self.client.get_channel(797955245665157152)
        #                 await channel.send(data)

        self.client.run(self.TOKEN)

