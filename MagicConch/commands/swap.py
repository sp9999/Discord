import utility


# ---------------------------------------------------------------------------------
#
# Description:  Help decipher and split up text from the !swap trigger
#
# ---------------------------------------------------------------------------------
def decipher_swap_string(message):  # param_string = !swap <nick> <line1> <line2>
    param_string = message.content

    splitList = param_string.split()
    if len(splitList) != 4:
        return "Usage: !swap <nick> <#1> <#2>"

    cmd, nick, line1, line2 = splitList

    return swapwb_cmd(message.server.name, nick, line1, line2)  # Call swapwb_cmd(<nick>, <line1>, <line2)


# ---------------------------------------------------------------------------------
#
# Usage #1:     swapwb_cmd(<nick>, <#1>, <#2>)
# Result:       Swaps <#1>-th line with <#2>-th line from <nick>.txt when an op, hop, or
#                   user in the whitelist uses the function
#
# ---------------------------------------------------------------------------------
def swapwb_cmd(server, param_nick, param_line_1, param_line_2):
    nick = utility.linkcheck(server, param_nick)
    line = None

    if param_line_1.isdigit() and param_line_2.isdigit():
        line = wb_swap(server, nick, int(param_line_1), int(param_line_2))
    else:
        return "Usage: !swap <nick> <#1> <#2>"

    if line is None:
        line1 = int(param_line_1)
        line2 = int(param_line_2)
        if line1 == 0 or line2 == 0:
            return "Line entries should not be 0"
        elif line1 == line2:
            return "Sounds like a useless operation, fam"
        else:
            return "File %s does not exist or entry out of bounds" % nick

    return "New swapped line from %s file at position %d: |%s|" % (nick, int(param_line_2), line)


# ---------------------------------------------------------------------------------
#
# Description:  Reads a <file> and prints out a line. Can specify which line and search terms
# Return:       Formatted line dictating line entry
#
# ---------------------------------------------------------------------------------
def wb_swap(server, param_file, param_line_1, param_line_2):

    if param_line_1 is 0 or param_line_2 is 0 or param_line_1 == param_line_2:
        return None

    line1 = param_line_1 - 1
    line2 = param_line_2 - 1
    fileName = utility.getFile(server, param_file)
    tempFile = utility.getFile(server, "temp")

    return utility.recreateFileAndSwapLines(fileName, tempFile, line1, line2)


def ex(message):
    return decipher_swap_string(message)
