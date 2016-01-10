# text.py - Part of pi2bot, by ngbeslhang
# NOTE: Those with * are done.
# TO-DO LIST:
#   - Bot kill and start command for the bot and add a trigger function + boolean.
#       - Which means a bot can be killed yet staying online so that owner can restart it.
#       * Will also include totalkill command (closing the entire Python script and make bot offline)
#   - Ownersnip system for certain commands w/ owner-checking function which returns boolean value. (Inspired by SexualRhinoceros' Musicbot)
#       - Which also allow creation of whitelist command for certain commands.
#           - ...which also leads to an idea of bot's permission system.
#           - Command that toggles no permission message, disabled by default.
#   - Timeout function which check which commands to time out with a list (be it array, external file etc.)
#   - Bot language switcher.
#   - Command that allow owner/whitelist to disable and enable other commands (not itself)
#   - Command that allow owner to add a new command for simple purpose/code. (If possible)

import discord
import asyncio

bot = discord.Client()

# You can rewrite on_ready() to anything you want.
@bot.async_event
def on_ready():
    print('Connected!')
    print('\tDiscord username: ' + bot.user.name)
    print('\tDiscord ID: ' + bot.user.id)

@bot.async_event
def on_message(message):
    # From discord.py's example codes, returns if the message author is bot itself.
    if message.author == bot.user:
        return
    
    # pi2bot uses @mention command prefix, thought might add other custom prefix templates outside bot's code.
    # Kudos to Hornwitser and Nerketur for helping me on prefix and teaching me more about Python!
    if len(message.mentions) == 1 and message.mentions[0] == bot.user:
        if message.content.startswith(bot.user.mention):
            cmd = message.content[len(bot.user.mention)+1:]
            
            # Commands
            # Display your Discord ID on console
            if cmd == 'myid':
                print(message.author.id)
            # kill - Kill the bot's Python script process
            if cmd == 'kill':
                if check_ownership(message, cmd, True) == True:
                    yield from bot.send_message(message.channel, "Forcekilling the bot.")
                    bot.close()
                    loop.close()
# Ownership/Permission system
# check_ownership() - Check the ID of message's author and compare it with a string.
# no_perm() - Send message to user that s/he do not have permission to use the command.         
def check_ownership(msg, cmd, display_msg = False):
    # Remember to add ID into owner.
    owner = ''
    if msg.author.id == owner:
        print('Owner ' + msg.author.name + '(' + msg.author.id + ') is using ' + cmd + '.')
        return True
    else:
        if display_msg == True:
            no_perm(msg)

def no_perm(msg):
    bot.send_message(msg.channel, 'Sorry ' + msg.author.mention + ', you do not have permission to use the command.')
            
# The part below is from discord.py's quickstart.
def main():
    print('Connecting...')
    # REMEMBER TO EDIT THE CODE BELOW!
    yield from bot.login('email', 'password')
    yield from bot.connect()
    
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
except Exception:
    loop.run_until_complete(bot.close())
finally:
    loop.close()