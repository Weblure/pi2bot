# WARNING: YOU NEED PYTHON 3.5 OR ABOVE IN ORDER TO USE PI2BOT MODULE.
import discord
import asyncio
import os
from sys import platform as _plat

# Python files import section reserved
# test

# Global variables declaration
bot = discord.Client()
owner_id = 'id'
filename = 'filename'

enabled = True
disabled_msg_count = 0

# NOTE: filename will not be used for now since there's a problem trying to assign the value to it.
# Command used for "restart"
if _plat in ('linux', 'linux2'):
    #restart_cmd = 'python3 ' + filename
    restart_cmd = 'python3 main.py'
else: #_plat == 'win32':
    #restart_cmd = 'python ' + filename
    restart_cmd = 'python main.py'

# Initializer
def init(email, passwd, id):
    global owner_id
    owner_id = id
    bot.run(email, passwd)
    
@bot.async_event
def on_ready():
    print('Connected!')
    print('\tDiscord username: ' + bot.user.name)
    print('\tDiscord ID: ' + bot.user.id)
    print('\tOwner\'s Discord ID: ' + owner_id)
    
# on_message()
@bot.async_event
async def on_message(msg):
    if msg.author == bot.user:
        return
    
    if len(msg.mentions) == 1 and msg.mentions[0] == bot.user:
        if msg.content.startswith(bot.user.mention):
            cmd = msg.content[len(bot.user.mention)+1:]
            is_owner = owner_check(msg)
            
            # If the bot is disabled this will display.
            if cmd[6:] not in ('enable', 'disable') and enabled == False:
                if is_owner == True:
                    await bot.send_message(msg.channel, 'Currently disabled, please type \"' + bot.user.mention + ' owner enable\".')
                # Set the count "disabled" message will display before it reach the number and stop.
                elif disabled_msg_count != 3:
                    await bot.send_message(msg.channel, 'Currently disabled, please contact the bot owner.')
                    disabled_msg_count = disabled_msg_count + 1
                return
            
            # Owner-only section
            if cmd[:6] == 'owner ':
                if is_owner == True:
                    await owner_cmd(cmd[6:], msg)
                else:
                    nopermmsg = 'Sorry ' + msg.author.mention + ', you do not have permission to use the command.'
                    await bot.send_message(msg.channel, nopermmsg)
            
# Command section
@bot.async_event
async def owner_cmd(cmd, msg):
    global enabled
    if cmd == 'kill':
        await bot.send_message(msg.channel, 'Killing...')
        await bot.logout()
    if cmd == 'restart':
        await bot.send_message(msg.channel, 'Restarting, please wait for at least 10 seconds.')
        os.system(restart_cmd)
        await bot.logout()
    if cmd == 'disable':
        await bot.send_message(msg.channel, 'Disabling...')
        enabled = False
    if cmd == 'enable':
        await bot.send_message(msg.channel, 'Enabling...')
        enabled = True
        disabled_msg_count = 0

# Permission section
def owner_check(msg):
    if msg.author.id == owner_id:
        return True
    else:
        return False
    