import os
from subprocess import Popen, PIPE, run, check_output
from discord.ext import commands
from dotenv import load_dotenv
from asyncio import sleep
from pyperclip import copy
import discord 
from discord import app_commands

# .env variables
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))
SERVER_DIR = os.getenv('SERVER_DIR')

# server directory to run commands from
# os.chdir(SERVER_DIR)
server_running = False


intents = discord.Intents.default()
intents.message_content = True
# main bot class object
bot = commands.Bot(command_prefix='=', help_command=None, intents=intents)


@bot.event
async def on_ready():
    print('server loaded on:')
    for guild in bot.guilds:
        print(f'{guild.name} | {guild.id}')

    try:
        synced = await bot.tree.sync()
    except Exception as e:
        print(e)


# @bot.tree.command(name='abrir')
async def open_server(ctx, *args: str):
    # main server on off variable
    global server_running
    if not server_running:

        # initial args
        start_command = 'java -Xms1024M -Xmx2048M -jar minecraft_server.1.12.2.jar'
        if 'gui=True' not in args:
            start_command += ' nogui'

        # main command shell
        global cmd
        cmd = Popen(start_command, shell=True, stdout=PIPE, stdin=PIPE)

        server_running = True
        print('SERVER OPEN')
        responses = ['Loading', 'Done', 'Exception', 'Stopping']

        for output in iter(cmd.stdout.readline, ''):
            if cmd.poll() is None:

                if output != '':
                    final_output = output.decode().rstrip()
                    print(final_output)

                    if 'debug=True' in args:
                        await ctx.send(final_output)

                    else:
                        for keyword in responses:
                            if keyword in final_output:
                                response_num = responses.index(keyword)

                                # responses
                                if response_num == 0:
                                    open_msg = await ctx.send('abrindo . . .')

                                elif response_num == 1:
                                    await open_msg.delete()
                                    await ctx.send('aberto em ' + final_output[39:final_output.find(')')])
                                    break

                                elif response_num == 2:
                                    await ctx.send(final_output)

                                elif response_num == 3:
                                    await ctx.send('fechando . . .')
                                    cmd.terminate()
                                    server_running = False

            else:
                server_running = False
                await ctx.send('fechado')


# @bot.tree.command(name='aberto?')
async def is_server_open(ctx):
    if server_running:
        await ctx.send('sim')
    else:
        await ctx.send('nao')


# @bot.tree.command(name='fechar')
async def close_server(ctx):
    if server_running:
        close_msg = await ctx.send('fechando . . .')
        print('SERVER CLOSE')
        cmd.communicate('stop'.encode())
        cmd.terminate()
        await close_msg.delete()
        await ctx.send('fechado')
    else:
        await ctx.send('server já fechado')


# DOES NOT WORK YET
# @bot.tree.command(name='cmd')
async def command_server(ctx, *command: str):
    pass
    # cmd.stdin.write(''.join(command).encode())
    await ctx.send(run(''.join(command), shell=True))


# @bot.tree.command(name='logout')
async def logout(ctx):
    await ctx.send('tchau')
    global server_running
    server_running = False
    await bot.logout()


# @bot.tree.command(name='help')
async def help(ctx):
    await ctx.send('fodase')


@bot.tree.command(name='ping')
async def ping(ctx):
    await ctx.response.send_message(f'POING ({round(bot.latency * 1000, 4)}ms)', ephemeral=True)


# @bot.event
async def on_error(event, *args, **kwargs):
    with open('error.log', 'w') as f:
        if event == 'on_message':
            f.write(f'{args[0]}')
            await guild.system_channel.send(f'`{args[0]}`')
        else:
            raise


# @bot.tree.command(name='search')
async def trr_search(ctx, *args):
    search_args = ' '.join(args)
    search = Popen(fr'trr dscd {search_args}', shell=True, stdout=PIPE)
    await sleep(5)
    search.terminate()

    output = ''.join([line.decode() for line in search.stdout.readlines()][2:-2])
    print(output)

    await ctx.send(output)

print('token:',TOKEN)
bot.run(TOKEN)

