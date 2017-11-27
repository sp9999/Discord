import utility
import config


# ---------------------------------------------------------------------------------
#
# Description:  Help decipher and split up text from the !rem trigger
#
# ---------------------------------------------------------------------------------
def decipher_rem_string(message):  # param_string = !rem <nick> <entry>
    param_string = message.content

    splitList = param_string.split(" ", 2)
    if len(splitList) != 3 or not splitList[2]:
        return "Usage: !rem <nick> <entry# or string>"

    cmd, name, string = splitList

    if name == "excuse":  # !rem excuse <1/2/3> <string>
        splitList = string.split(" ", 1)  # splitList = [<1/2/3>, <string>]
        excuseIndex = int(splitList[0])

        if len(splitList) != 2 or not splitList[1] or excuseIndex < 1 or excuseIndex > 3:  # no second half
            return "Usage: !rem excuse <1:start 2:subject 3:problem> <entry# or string>"

        excuseFiles = ["estart", "esubject", "eproblem"]
        name = excuseFiles[excuseIndex - 1]  # name = <estart/esubject/eproblem>
        string = splitList[1]  # string = <string>

    doMaster = name not in config.AllSpecialFiles

    return removewb_cmd(message.server.name, name, string, doMaster)  # Call removewb_cmd(<nick>, <entry>)


# ---------------------------------------------------------------------------------
#
# Usage #1:     removewb_cmd(<nick>, <#>)
# Result:       Removes <#>-th line from <nick>.txt when an op, hop, or
#                   user in the whitelist uses the function
#
# Usage #2:     removewb_cmd(<nick>, #)
# Result:       Removes last line from <nick>.txt
#
# Usage #3:     removewb_cmd(<nick>, <string>)
# Result:       Removes <string> from <nick>.txt
#
# ---------------------------------------------------------------------------------
def removewb_cmd(server, param_nick, param_entry, param_doMaster = True):
    nick = utility.linkcheck(server, param_nick)
    line = wb_remove(server, nick, param_entry, param_doMaster)

    if line is None:
        return "File %s does not exist" % nick

    if param_entry == '#':
        if len(line) > 0:
            return "Removing last entry from %s: |%s|" % (nick, line)
        else:
            return "No entries exist for %s." % nick
    elif param_entry.isdigit():
        if len(line) > 0:
            return "Removing line number %d from %s: |%s|" % (int(param_entry), nick, line)
        else:
            return "Entry number %d does not exist." % int(param_entry)
    else:
        if line and len(line) > 0:
            return "Removing line from %s: |%s|" % (nick, line)
        else:
            return "Line does not exist in %s. Already removed!" % nick


# ---------------------------------------------------------------------------------
#
# Description:  Removes a line from <nick>.txt. Can specify which line and search terms
# Return:       Removed line
#
# ---------------------------------------------------------------------------------
def wb_remove(server, param_nick, param_entry, param_doMaster=True):
    masterFile = utility.getFile(server, config.MasterFile[0])
    fileName = utility.getFile(server, param_nick)
    tempFile = utility.getFile(server, "temp")

    removeLine = None
    removeLastLine = False
    removeLineNo = None

    if param_entry == '#':
        removeLastLine = True
    elif param_entry.isdigit():
        removeLineNo = int(param_entry)
    else:
        removeLine = param_entry

    masterFileLineToBeRemoved = utility.remove(fileName, tempFile, removeLastLine, removeLineNo, removeLine)
    if not masterFileLineToBeRemoved:
        return "File not found"

    if param_doMaster:
        utility.remove(masterFile, tempFile, None, None, masterFileLineToBeRemoved)

    return masterFileLineToBeRemoved


def ex(message):
    return decipher_rem_string(message)
