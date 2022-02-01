import discord
from BotToken import TOKEN
from discord.ext import commands

from db_connection import *
from db_settings import settings

intents = discord.Intents.default()
intents.presences = True
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print('We have successfully loggged in as {0.user}'.format(client))


@client.command(name='free')
async def park_place(ctx):
    channel = ctx.channel

    print("TEST")
    await channel.send(file=discord.File('image2new.jpg'))


@client.command(name='come_over_here')
async def join_channel(ctx):
    channel = ctx.author.voice.channel
    print(channel.id)
    await channel.connect()


@client.command(name='go_away')
async def leave_channel(ctx):
    channel = ctx.author.voice.channel
    print(channel.id)
    await ctx.voice_client.disconnect()


@client.command(name='my_mess')
async def get_users_mess(ctx):
    connection = DBSession(settings)
    records = connection.GetUserMessage(ctx.author.display_name + ctx.author.discriminator)

    for mess in records:
        await ctx.channel.send(ctx.author.display_name + ' ' + mess)


@client.event
async def on_message(message):
    # print(message.author.discriminator)
    if message.author == client.user:
        return

    print(message.content)
    if message.content[0] != '!':
        connection = DBSession(settings)
        connection.WriteUserMessage(message.author.display_name + message.author.discriminator, message.content)

    if message.content.lower() == 'hello':
        await message.channel.send(f'Hello, {message.author.display_name}! , are you {message.author.activity}?')
        connected = message.author.voice
        if connected:
            await connected.channel.connect()
        return

    if message.content.lower() == 'bye':
        await message.channel.send(f'See you later, {message.author.display_name}!')
        return

    await client.process_commands(message)


@client.event
async def on_group_join(channel, user):
    channel.send(f'Hi, {user.display_name}, are you {user.activity}?')


@client.event
async def on_member_join(member):
    print(member)


client.run(TOKEN)
