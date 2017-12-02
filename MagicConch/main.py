#!/usr/bin/python2
from discord.ext.commands import Bot
import discord
import logging
import config
import secret
import commands.wb
import commands.excuse
import commands.swap
import commands.add
import commands.rem
import commands.timer
import commands.info
import utility
import QuoteTimer
import re

# Setup client
bot_prefix = "!"
client = Bot(command_prefix=bot_prefix)

# Setup logging
log = logging.getLogger('discord')
logging.basicConfig(level=logging.ERROR)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
log.addHandler(handler)


@client.event
async def on_ready():
    print("Logged in as %s, id:  %s" % (client.user.name, client.user.id))
    await client.change_presence(game=discord.Game(type=0, name="SP's quotebot | !help"))
    for s in client.servers:
        QuoteTimer.QuoteTimer(client, s).setup()
        print("  - %s (%s)" % (s.name, s.id))


@client.command(pass_context=True, brief="Reads a line from a file")
async def wb(ctx):
    """
        Usage: !wb <nick> <line no. or '#'> <search term> - Line from <nick> file.
        Line: specifies line entry or the latest entry ('#').
        Search: Anything after <line param> specifies only lines containing <search term>.
        Optional: You can omit <nick> to use the master file which will grab from all possible quotes.
    """
    if not utility.isAllowedEnvironment(ctx.message):
        return

    string = commands.wb.ex(ctx.message)
    if string:
        await client.say(utility.textBlock(string))


@client.command(pass_context=True, brief="Gets original owner of a line from the master database")
async def info(ctx):
    """
        Usage: !info <line no. or '#'> - Same as !wb <#>, but gives you information about the owner of the line
        Usage: !info build - Recreates info.txt with all the information about line owners
            - ONLY USABLE BY BOT OWNER!
            - Requires reading through all the files. Should not be used except the first time for a server!
    """
    if not utility.isAllowableServer(ctx.message.server.name):
        return

    string = commands.info.ex(ctx.message)
    if string:
        await client.say(utility.textBlock(string))


@client.command(pass_context=True, brief="Generates an excuse")
async def excuse(ctx):
    """
        Usage: !excuse <#1> <#2> <#3> - Generate a random excuse from three files (start, subject, problem).
            Line: You can specify every entry no. for the three parts. '#' will use the latest entry.
            Line: Use 0 for random for any entry. Ex: !excuse 0 0 # for only latest problem entry, the rest random.

        Add: !add excuse <1/2/3> <string> - Add new line to one of the three excuse files.
        Rem: !rem excuse <1/2/3> <string/#> - Remove line (either string matching or entry no.) from one of the three excuse files.
        Format - <I didn't X because> <subject verb> <reason>.
        Example - <I couldn't finish because> <I was> <working/drunk/being X>
    """
    if not utility.isAllowedEnvironment(ctx.message):
        return

    string = commands.excuse.ex(ctx.message)
    if string:
        await client.say(utility.textBlock(string))


@client.command(pass_context=True, brief="Swaps two lines in a file. (Requires permissions)")
async def swap(ctx):
    """
        Usage: !swap <nick> <#1> <#2>
            - Useful if want to memorize WB #'s easier.
    """
    if not utility.isAllowableServer(ctx.message.server.name):
        return

    if not utility.whitelist(ctx.message.server.name, ctx.message.author):
        return

    string = commands.swap.ex(ctx.message)
    if string:
        await client.say(utility.textBlock(string))


@client.command(pass_context=True, brief="Add a line to a file (Requires permissions)")
async def add(ctx):
    """
        Usage: !add <nick> <string>
        Usage: !add whitelist <nick> - used to give permission for add/rem commands
        Usage: !add link <alt-nick> <nick> - allows redirect so that doing !wb <alt-nick> does !wb <nick> instead
        Usage: !add excuse <1:start 2:subject 3:problem> <string>
        Usage: !add ignore_channel <channel name> - prevents public commands (!wb, !excuse) from working in that channel
    """
    if not utility.isAllowableServer(ctx.message.server.name):
        return

    if not utility.whitelist(ctx.message.server.name, ctx.message.author):
        return

    string = commands.add.ex(ctx.message)
    if string:
        await client.say(utility.textBlock(string))


@client.command(pass_context=True, brief="Removes a line to a file (Requires permissions)")
async def rem(ctx):
    """
        Usage: !rem <nick> <#/string> - remove entry either by number or text matching from a file
            - You can also remove from 'whitelist', 'link', 'ignore_channel' if passed as <nick>

        Usage: !rem excuse <1:start 2:subject 3:problem> <#/string>
    """
    if not utility.isAllowableServer(ctx.message.server.name):
        return

    if not utility.whitelist(ctx.message.server.name, ctx.message.author):
        return

    string = commands.rem.ex(ctx.message)
    if string:
        await client.say(utility.textBlock(string))


@client.command(pass_context=True, brief="Sets timer setting for occasional quote from bot (Requires permissions)")
async def timer(ctx):
    """
        Usage: !timer time <number in seconds> - frequency of messages (0 is disable feature)
            - Re-enabling the timer (from 0) could take up to 10 minutes before change is picked up, so be patient!

        Usage: !timer channel <channel name (case sensitive) - channel that messages should be published in
        Usage: !timer - gets info for QuoteTimer
    """
    if not utility.isAllowableServer(ctx.message.server.name):
        return

    if not utility.whitelist(ctx.message.server.name, ctx.message.author):
        return

    string = commands.timer.ex(ctx.message)
    if string:
        await client.say(utility.textBlock(string))


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if len(message.mentions) > 0:
        for user in message.mentions:
            if user.name == secret.BOT_NAME:
                if message.author.name == secret.BOT_OWNER:
                    remaining = message.content.split(" ", 1)
                    if len(remaining) > 1 and (remaining[1] == "quit" or remaining[1] == " quit"):
                        client.logout()
                        exit(1)

                if not utility.isAllowedEnvironment(message):
                    return

                string = commands.wb.ex_with_params(message.server.name)
                if string:
                    await client.send_message(message.channel, utility.textBlock(string))
                    return

    if message.content.upper().find(config.SEMEN_DEMON[0].upper()) is not -1:
        string = commands.wb.ex_with_params(message.server.name, config.SEMEN_DEMON[1])
        await client.send_message(message.channel, utility.textBlock(string))

    count = 0
    for trigger in secret.SecretTriggerWords[message.server.name]:
        compiled = re.compile(trigger, re.IGNORECASE)
        result = compiled.search(message.content)
        if result is not None:
            response = secret.SecretTriggerWordsResponse[message.server.name][count]
            await client.send_message(message.channel, utility.textBlock(">" + response))
        count += 1

    await client.process_commands(message)


client.run(secret.TOKEN)

