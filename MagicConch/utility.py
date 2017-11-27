import random
import config
import secret
import os


# ---------------------------------------------------------------------------------
#
# Description:  Reads a <file> and returns a line. Can specify which line and search terms
# Return:       Line, (relative if key) line entry, total (key) lines, key line entry, total lines
#
# ---------------------------------------------------------------------------------
def read_file(param_file, param_count=None, param_key=None):
    if not doesFileExist(param_file):
        return

    lines = []
    keylines = []
    lineIt = 1
    keyIt = []

    with open(param_file, encoding="utf8") as fp:
        for line in fp:
            if param_key is not None:
                if line.upper().find(param_key.upper()) is not -1:
                    keylines.append(line)
                    keyIt.append(lineIt);
            lines.append(line)
            lineIt += 1

    totalcount = len(lines)
    if totalcount is 0:
        if param_key is None:
            return "No entries found", 0, 0
        else:
            return "No entries found", 0, 0, 0, 0

    if param_key is None:
        if param_count is None:
            param_count = random.randint(0, totalcount)
        elif param_count is '#':
            param_count = totalcount - 1
        elif param_count.isdigit():
            param_count = int(param_count) - 1
        else:
            return "Invalid input. Expected digit.", 0, 0
    else:
        totalcount = len(keylines)
        if totalcount is 0:
            return "No occurences of '%s' could be found." % param_key, -1, 0, 0, 0

        if param_count is '#':
            param_count = random.randint(0, totalcount)
        elif param_count.isdigit():
            param_count = int(param_count) - 1
        else:
            return "Invalid input. Expected digit.", 0, 0, 0, 0

    if param_count >= totalcount:
        param_count = totalcount - 1

    finalcount = param_count
    if param_key is not None:
        return keylines[finalcount][:-1], finalcount + 1, totalcount, keyIt[finalcount], len(lines)

    return lines[finalcount][:-1], finalcount + 1, totalcount


def recreateFileAndSwapLines(filename, tempfile, line1, line2):
    if not doesFileExist(filename):
        return None

    with open(filename, encoding="utf8") as fp:
        lines = fp.readlines()

    totalcount = len(lines)
    if totalcount is 0:
        return None

    if line1 >= totalcount or line2 >= totalcount:
        return None

    # Copy all lines from <nick>.txt into temp.txt except the line we are removing
    with open(tempfile, "w", encoding="utf8") as outputFile:
        for lineCount in range(totalcount):
            outputLine = lines[lineCount]

            if lineCount == line1:
                outputLine = lines[line2]
            elif lineCount == line2:
                outputLine = lines[line1]

            for i in range(3):
                try:
                    outputFile.write(outputLine)
                    break
                except OSError:
                    print("Failure at swapping \"%s\" on attempt %s" % (outputLine, i))

    removeAndRenameFile(filename, tempfile)

    return lines[line1][:-1]


# ---------------------------------------------------------------------------------
#
# Description:  Remove a line from <file> and returns the deleted line. Can specify which line
# Return:       Removed line
#
# ---------------------------------------------------------------------------------
def remove(param_file, param_tempfile, param_lastline=False, param_entryno=None, param_line=None):
    if not doesFileExist(param_file):
        return None

    removedLine = ""

    # Copy all lines from <nick>.txt into temp.txt except the line we are removing
    with open(param_file, encoding="utf8") as inputFile:
        with open(param_tempfile, "w", encoding="utf8") as outputFile:
            lineCount = 0
            previousLine = ""
            skip = False
            for line in inputFile:
                if len(previousLine) > 0:
                    if isRemoveLineFound(param_entryno, lineCount, param_line, previousLine[:-1]):
                        removedLine = previousLine
                        skip = True

                if not skip:
                    for i in range(3):
                        try:
                            outputFile.write(previousLine)
                            break
                        except OSError:
                            print("Failure at writing \"%s\" on attempt %s" % (previousLine, i))

                lineCount += 1
                previousLine = line
                skip = False

                if isRemoveLineFound(param_entryno, lineCount, param_line, previousLine[:-1]):
                    removedLine = line

            if param_lastline:
                removedLine = previousLine
            elif lineCount != param_entryno and param_line != previousLine[:-1]:
                for i in range(3):
                    try:
                        outputFile.write(previousLine)
                        break
                    except OSError:
                        print("Failure at writing \"%s\" on attempt %s" % (previousLine, i))

    removeAndRenameFile(param_file, param_tempfile)

    return removedLine[:-1]


def isRemoveLineFound(remove_lineno, curr_lineno, remove_line, curr_line):
    if curr_lineno and remove_lineno and curr_lineno == remove_lineno:
        return True
    elif curr_line and remove_line and curr_line == remove_line:
        return True
    return False


def removeFile(filename):
    for i in range(3):
        try:
            os.remove(filename)
            break
        except OSError:
            print("Error in removing \"%s\"" % filename)
            continue


def removeAndRenameFile(filename, tempfile):
    # Delete <filename>.txt and rename temp.txt into <filename>.txt
    removed = False
    for i in range(3):
        try:
            if not removed:
                os.remove(filename)
                removed = True
        except OSError:
            print("Error in removing \"%s\"" % filename)
            continue

        try:
            os.rename(tempfile, filename)
            break
        except OSError:
            print("Error in renaming \"%s\"" % filename)


def doesFileExist(filename):
    # Guarantee file exists
    try:
        fp = open(filename)
    except IOError:
        return False
    fp.close()
    return True


# ---------------------------------------------------------------------------------
#
# Description:  Check if <altnick> is a different name for a user
# Return:       Either the original <nick> if found, or unmodified <altnick>
# Note:         Database (link.txt) expects entries in the form of <altnick> <nick> per line
#
# ---------------------------------------------------------------------------------
def linkcheck(server, param_altnick):
    file = getFile(server, config.UtilityFiles[0], False)
    if not doesFileExist(file):
        return param_altnick

    with open(file, encoding="utf8") as fp:
        for line in fp:
            if line.upper().find(param_altnick.upper()) is not -1:
                space = line.find(' ')
                if line.upper()[:space] == param_altnick.upper():
                    name = line[space + 1:-1]
                    return name
    return param_altnick


# ---------------------------------------------------------------------------------
#
# Description: Checks if <nick> exists in whitelist.txt
# Returns:     True or False
#
# ---------------------------------------------------------------------------------
def whitelist(server, author):
    permissions = author.top_role.permissions
    if permissions.administrator or permissions.manage_server or permissions.manage_channels or permissions.manage_roles:
        return True

    file = getFile(server, config.UtilityFiles[1])

    if not doesFileExist(file):
        return False

    name = linkcheck(server, author.name)

    with open(file, encoding="utf8") as fp:
        for line in fp:
            if line.upper()[:-1] == name.upper():
                return True
            for role in author.roles:
                if line.upper()[:-1] == role.name.upper():
                    return True
    return False


# ---------------------------------------------------------------------------------
#
# Description:  Gets <filename>.txt with full path
#
# ---------------------------------------------------------------------------------
def getFile(server, filename=None, checkLink=True):
    path = attemptToGetPath(server)

    if filename:
        if checkLink:
            filename = linkcheck(server, filename)
        file = path + filename + ".txt"
    else:
        file = path + config.MasterFile[0] + ".txt"
    return file


def isAllowableServer(server):
    return secret.DiscordToHexchatMap.get(server) is not None


def isAllowableChannel(server, channel):
    file = getFile(server, config.UtilityFiles[2])
    if doesFileExist(file):
        with open(file, encoding="utf8") as fp:
            for line in fp:
                if line.strip() == channel:
                    return False
        return True

    ignoredChannels = secret.ServerDefaultIgnoreChannels.get(server)
    for bannedChannel in ignoredChannels:
        if bannedChannel == channel:
            return False
    return True


def isAllowedEnvironment(message):
    if message.server is not None:
        return isAllowableServer(message.server.name) and isAllowableChannel(message.server.name, message.channel.name)
    return False


# ---------------------------------------------------------------------------------
#
# Description:  Check if <server> maps to a known hexchat server
# Return:       Either the original <path> is returned, or unmodified <path>
# Note:         Database (link.txt) expects entries in the form of <altnick> <nick> per line
#
# ---------------------------------------------------------------------------------
def attemptToGetPath(serverName):
    path = secret.DiscordToHexchatMap.get(serverName)
    if not path or path is False:
        path = "wb\\" + serverName + "\\"
    return path


def getServerTimerChannel(server):
    file = getFile(server.name, config.UtilityFiles[3])
    channelName = None
    if doesFileExist(file):
        with open(file, encoding="utf8") as fp:
            for line in fp:
                channelName = line.strip()

    if channelName is None:
        channelName = secret.ServerDefaultTimerChannel[server.name]

    for channel in server.channels:
        if channelName == channel.name:
            return channel
    return None


def getServerTimer(serverName):
    file = getFile(serverName, config.UtilityFiles[4])
    if doesFileExist(file):
        with open(file, encoding="utf8") as fp:
            for line in fp:
                return int(line.strip())
    return secret.ServerDefaultTimer[serverName]


def textBlock(string):
    return '```css\n' + string + '```'
