import os
import discord
import argparse
import io
import aiohttp
from dotenv import load_dotenv

# python DiscordSA.py --ip 192.168.56.1 --port 8000

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

print("Token:", TOKEN)
print("Guild:", GUILD)

client = discord.Client()

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ip", type=str, required=True,
                help="ip address of the device")
ap.add_argument("-o", "--port", type=int, required=True,
                help="ephemeral port number of server (1024, to 65535)")
args = vars(ap.parse_args())
serverLocation = "http://" + str(args["ip"]) + ":" + str(args["port"])

print("Server location: " + serverLocation)


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            print("Equal!")
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.event
async def on_message(message):
    channel = client.get_channel(797955245665157152)
    if message.author == client.user:
        return

    # User asked for count
    if message.content == '!count':
        response = "I found this many boxes!"
        channel = client.get_channel(797955245665157152)
        await channel.send(response)

    # User asked for screenshot
    if message.content == "!image":
        async with aiohttp.ClientSession() as session:
            # Request image
            async with session.get(serverLocation + "/single.jpg") as resp:

                # No image found!
                if resp.status != 200:
                    return await channel.send('Could not download file...')

                # Read response and send data to channel
                data = io.BytesIO(await resp.read())
                await channel.send(file=discord.File(data, 'screenshot.jpg'))

    # User asked for boxes
    if message.content == '!boxes':
        async with aiohttp.ClientSession() as session:
            async with session.get(serverLocation + "/boxes") as resp:

                # Nothing found
                if resp.status != 200:
                    return await channel.send('Could not download file...')

                # "utf-8" part removes b'<data>' and automatically formats
                data = str(await resp.read(), "utf-8")
                channel = client.get_channel(797955245665157152)
                await channel.send(data)

client.run(TOKEN)
