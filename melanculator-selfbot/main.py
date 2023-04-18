from dotenv import load_dotenv
from os import getenv
import json

import discord
from discord.ext import commands

# --- INITIALISE ---
load_dotenv()
token = getenv('SELF_TOKEN')
print('token: ' + token)


bot = commands.Bot('$', self_bot=True, help_command=None)

# --- LOAD CONFIG ---
try:
    f = open('saved_data.json')
except FileNotFoundError:
    print('assign channel / dm with `assign`')
else:
    save = json.load(f)
    print(save)
    f.close()


# --- EVENTS ---
@bot.event
async def on_ready():
    print(f'READY\n{save["emoji_select"]} LOADED ON CHANNELS')
    for channel in save['channels']:
        print('* ', channel)
    print()


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.channel.id in save['channels']:
        for emoji in save['emoji_select']:
            await message.add_reaction(emoji)


# --- COMMANDS ---
@bot.command('help')
async def help_cmd(ctx):
    await ctx.message.delete()
    await ctx.send(r'''```js
==========[ MELANCULATOR 1.0 BUILD 4 ]==========

................................................
................................................
........................................:**.....
............................::::*******VV$V.....
.................::::******************VF$*.....
........*V*****************************VNM......
.......:*NNV***********************:**VI$*......
......::::MNV********************::**VV$F.......
.....::::::MNV**:**:**.*************VV$I........
.....:::::::F$FV**********::*::****VI$F.........
......:::::::*NMV****************VVMN*..........
........::::::*VNMVV**********VVFNMV:...........
.........:::::::*VMNMIVVVVVVFMNMV*:.............
............:::::::**VIMMMMIV**:................
...............:::::::::::::....................
................................................
................................................

==================[ COMMANDS ]==================

                    prefix: $                   
                  * = optional                  

emoji <emoji(s)>        emojis to react on order

assign <*chat id>           react to single chat

append <*chat id>            add channel to list

remove <chat id>        remove channel from list

server           add all server channels to list

reset                 reset channel list to none

undercover <*f/t>                delete commands

stop                                  logout bot

help                                        this

================================================
```''')
    if save["undercover"]:
        await ctx.message.delete()


@bot.command('a')
async def announce(ctx):
    await ctx.send('''`==========[ M E L A N C U L A T O R ]===========
................................................
................................................
........................................:**.....
............................::::*******VV$V.....
.................::::******************VF$*.....
........*V*****************************VNM......
.......:*NNV***********************:**VI$*......
......::::MNV********************::**VV$F.......
.....::::::MNV**:**:**.*************VV$I........
.....:::::::F$FV**********::*::****VI$F.........
......:::::::*NMV****************VVMN*..........
........::::::*VNMVV**********VVFNMV:...........
.........:::::::*VMNMIVVVVVVFMNMV*:.............
............:::::::**VIMMMMIV**:................
...............:::::::::::::....................
................................................
................................................
==========[ M E L A N C U L A T O R ]===========
`''')
    await ctx.message.delete()


@bot.command('emoji')
async def select_emoji(ctx, emojis):
    print([emoji.strip() for emoji in emojis.split(' ')])
    emojis = [emoji.strip() for emoji in emojis.split(' ')]

    save["emoji_select"] = emojis

    f = open('saved_data.json', 'w')
    print(f'{save["emoji_select"]} EMOJI')
    json.dump(save, f)
    f.close()
    await ctx.message.delete()


@bot.command('assign')
async def assign_single_channel(ctx, *channel_id: int):
    if channel_id:
        user = await bot.fetch_user(channel_id[0])
        channel_id = user.dm_channel.id
        print(channel_id)
    else:
        channel_id = ctx.channel.id

    save['channels'] = [channel_id]
    print(f'{channel_id} ASSIGNED')
    f = open('saved_data.json', 'w')
    json.dump(save, f)
    f.close()

    if save["undercover"]:
        await ctx.message.delete()


@bot.command('append')
async def append_channel(ctx, *channel_id: int):
    if channel_id:
        user = await bot.fetch_user(channel_id[0])
        channel_id = user.dm_channel.id
        print(channel_id)
    else:
        channel_id = ctx.channel.id

    global save
    if channel_id not in save['channels']:
        save['channels'].append(channel_id)
        print(f'{channel_id} APPEND')
    else:
        print(f'{channel_id} ALREADY APPENDED')
    f = open('saved_data.json', 'w')
    json.dump(save, f)
    f.close()

    if save["undercover"]:
        await ctx.message.delete()


@bot.command('remove')
async def append_channel(ctx, *channel_id: int):
    if channel_id:
        user = await bot.fetch_user(channel_id[0])
        channel_id = user.dm_channel.id
        print(channel_id)
    else:
        channel_id = ctx.channel.id

    global save
    if channel_id in save['channels']:
        save['channels'].remove(channel_id)
        print(f'{channel_id} REMOVED')
    else:
        print(f'{channel_id} DOESN\'T EXIST')
    f = open('saved_data.json', 'w')
    json.dump(save, f)
    f.close()

    if save["undercover"]:
        await ctx.message.delete()


@bot.command('server')
async def server_append(ctx):
    for channel in ctx.guild.channels:
        if isinstance(channel, discord.TextChannel):

            save['channels'].append(channel.id)
    f = open('saved_data.json', 'w')
    json.dump(save, f)
    f.close()

    if save["undercover"]:
        await ctx.message.delete()


@bot.command('reset')
async def reset_channels(ctx):
    save['channels'] = []
    f = open('saved_data.json', 'w')
    json.dump(save, f)
    f.close()

    if save["undercover"]:
        await ctx.message.delete()


@bot.command('undercover')
async def delete_command(ctx, *bool: str):
    if bool:
        if bool == 'f':
            save["undercover"] = False
        if bool == 't':
            save["undercover"] = True
    else:
        save["undercover"] = True

    f = open('saved_data.json', 'w')
    json.dump(save, f)
    f.close()

    await ctx.message.delete()


# --- RUN ---
bot.run(token)
