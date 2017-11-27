import utility
import commands.add


def timerString(server):
    interval = utility.getServerTimer(server.name)
    if interval == 0:
        return "QuoteTimer for %s in #%s is currently disabled" % (server.name,
                                                                   utility.getServerTimerChannel(server))
    else:
        return "QuoteTimer for %s in #%s with a %d second interval" % (server.name,
                                                                   utility.getServerTimerChannel(server),
                                                                   interval)


# ---------------------------------------------------------------------------------
#
# Description:  Help decipher and split up text from the !timer trigger
#
# ---------------------------------------------------------------------------------
def decipher_timer_string(message):  # param_string = !timer <time/channel> <entry>
    param_string = message.content

    splitList = param_string.split(" ", 2)  # splitList = [!timer, <time/channel>, <entry>]
    if len(splitList) == 1:
        return timerString(message.server)

    elif len(splitList) != 3 or not splitList[2]:
        return "Usage: !timer <time/channel> <new value>"

    cmd, file, entry = splitList

    if file != "time" and file != "channel":
        return "Usage: !timer <time/channel> <new value>"

    return timer_cmd(message.server, "timer_"+file, entry)  # Call timer_cmd(<file>, <entry>)


# ---------------------------------------------------------------------------------
#
# Usage #1:     timerwb_cmd(<timer_time/timer_channel>, <new entry>)
# Result:       Deletes and writes new entry in file
#
# ---------------------------------------------------------------------------------
def timer_cmd(server, file, entry):

    if file == "timer_time" and entry.isdigit():
        value = int(entry)
        if value > (60 * 60 * 24 * 7):
            value = 0
        commands.add.addwb_cmd(server.name, file, str(value))
        return timerString(server)

    if file == "timer_channel":
        for channel in server.channels:
            if entry == channel.name:
                commands.add.addwb_cmd(server.name, file, entry)
                return timerString(server)
        return "No channel found for #" + entry

    return "Usage: !timer <time/channel> <new value>"


def ex(message):
    return decipher_timer_string(message)
