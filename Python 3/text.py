# text.py - Part of pi2bot, by ngbeslhang
# NOTE: Those with * are done.
# TO-DO LIST:
#   * Global bot disabling and enabling command. (Kudos to Hornwitser)
#       - Able to allow owner to disable individual commands
#       - Which means a bot can be killed yet staying online so that owner can restart it.
#       * Kill command (closing the entire Python script and make bot offline)
#   * Ownership system for certain commands. (Inspired by SexualRhinoceros' Musicbot)
#       - Which also allow creation of whitelist command for certain commands.
#           - ...which also leads to an idea of bot's permission system.
#           - Command that toggles no permission message, disabled by default.
#   - Timeout function which check which commands to time out with a list (be it array, external file etc.)
#   - Bot language switcher.
#   - Command that allow owner/whitelist to disable and enable other commands (not itself)
#   - Command that allow owner to add a new command for simple purpose/code. (If possible)
#   - PM-based invitation accept system which the owner can choose to accept or not.
#   - Help command which also list help for individial command if inserted as second parameter.
#       - Inspired by Red_M testing his bot, Frog's ,help command
#
# Kudos to Hornwitser, Nerketur and others at unofficial Discord API server's #python_discord-py for helping me teaching me more about Python!

import discord
import asyncio

# The global variables below are either from main() or for Ownership/Permission system
# They are put here for easiness to access and editing (due to extensive testing)
# REMEMBER TO CHANGE ALL OF THEM
email = 'email'
password = 'passwd'
owner_id = 'id'

bot = discord.Client()

# You can rewrite on_ready() to anything you want.
@bot.async_event
def on_ready():
    print('Connected!')
    print('\tDiscord username: ' + bot.user.name)
    print('\tDiscord ID: ' + bot.user.id)
    
is_disabled = False
disabled_msg_count = 0
    
@bot.async_event
def on_message(message):
    # Used to prevent "referenced before assignment" error, Hornwitser
    global is_disabled
    global disabled_msg_count
    
    # From discord.py's example codes, returns if the message author is bot itself.
    if message.author == bot.user:
        return
    
    # pi2bot uses @mention command prefix, thought might add other custom prefix templates outside bot's code.
    # Hornwitser
    if len(message.mentions) == 1 and message.mentions[0] == bot.user:
        if message.content.startswith(bot.user.mention):
            cmd = message.content[len(bot.user.mention)+1:]
            
            is_owner = check_ownership(message, cmd)
            # "cmd not in ()", Hornwitser
            if cmd not in ('enable', 'disable', 'check status') and is_disabled == True:
                if is_owner == True:
                    yield from bot.send_message(message.channel, 'Currently disabled, please reenable by typing \"' + bot.user.mention + ' enable\".')
                # Set the count "disabled" message will display before it reach the number and stop.
                elif disabled_msg_count != 1:
                    yield from bot.send_message(message.channel, 'Currently disabled, please contact the bot owner to reenable.')
                    disabled_msg_count = disabled_msg_count + 1
                return
            
            # This part is for owner-only commands.
            if is_owner == True and cmd in ('kill', 'enable', 'disable') or cmd[:5] in ('check'):
                if cmd == 'kill':
                    yield from bot.send_message(message.channel, 'Killing...')
                    cmd_kill()
                if cmd == 'enable' or 'disable':
                    if cmd == 'disable':
                        yield from bot.send_message(message.channel, 'Disabling...')
                        is_disabled = bot_toggle(cmd)
                    elif cmd == 'enable':
                        yield from bot.send_message(message.channel, 'Enabling...')
                        is_disabled = bot_toggle(cmd)
                        disabled_msg_count = 0
                if cmd[:5] == 'check':
                    if cmd[6:] == 'status':
                        if is_disabled == True:
                            status = 'Disabled'
                            disabled_msg_count = disabled_msg_count + 1
                        else:
                            status = 'Enabled'
                        yield from bot.send_message(message.channel, 'Bot status: ' + status)
                        
            elif is_owner == False and cmd in ('kill', 'enable', 'disable') or cmd[:5] in ('check'):
                yield from bot.send_message(message.channel, 'Sorry ' + message.author.mention + ', you do not have permission to use the command.')
            
            # This part is for public commands.
            else:
                if cmd == 'hello':
                    yield from bot.send_message(message.channel, 'Hello, ' + message.author.mention + '!')
                
# Bot toggle
def bot_toggle(cmd):
    if cmd == 'enable':
        return False
    elif cmd == 'disable':
        return True
                    
# Command functions
def cmd_kill():
    loop.run_until_complete(bot.close())
    loop.close()
                    
# Ownership/Permission system
# check_ownership() - Check the ID of message's author and compare it with a string.
# no_perm() - Send message to user that s/he do not have permission to use the command.         
def check_ownership(msg, cmd, display_msg = False):
    if msg.author.id == owner_id:
        print('Owner ' + msg.author.name + '(' + msg.author.id + ') is using ' + cmd + '.')
        return True
    else:
        print(msg.author.name + ' wanted to use ' + cmd + ' but do not have permission to do so.')
        return False
            
# The part below is from discord.py's quickstart.
def main():
    print('Connecting...')
    yield from bot.login(email, password)
    yield from bot.connect()
    
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
except Exception:
    loop.run_until_complete(bot.close())
finally:
    loop.close()