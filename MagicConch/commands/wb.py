import utility


# --------------------------------------------------------------------------------
#
# Description:  Help decipher and split up text from the !wb trigger
#
# --------------------------------------------------------------------------------
def decipher_wb_string(message):                            # param_string = !wb <nick> <#> <string>
    param_string = message.content
    splitList = param_string.split(" ", 1)                  # splitList = [!wb, <nick> <#> <string>]

    # wb.txt
    filename = utility.getFile(message.server.name)
    if len(splitList) != 2 or not splitList[1]:             # No other parameters
        line = wb_cmd(filename)                             # Call wb_cmd(wb)
    else:
        splitList = splitList[1].split(" ", 1)                  # splitList = [<nick>, <#> <string>]
        if splitList[0] is '#' or splitList[0].isdigit():       # in instance of [<#>, <string>]
            entryNo = splitList[0]                              # entryNo = <#>
            if len(splitList) != 2 or not splitList[1]:         # Only <#> as param
                line = wb_cmd(filename, entryNo)                # Call wb_cmd(wb, <#>)
            else:
                line = wb_cmd(filename, entryNo, splitList[1])  # Call wb_cmd(wb, <#>, <string>)
        else:
            nick = splitList[0]                                 # nick = <nick>
            if len(splitList) != 2 or not splitList[1]:       # Only <nick> as a param
                filename = utility.getFile(message.server.name, nick)
                line = wb_cmd(filename)                         # Call wb_cmd(<nick>)
            else:
                filename = utility.getFile(message.server.name, nick)
                splitList = splitList[1].split(" ", 1)              # splitList = [<#>, <string>]
                entryNo = splitList[0]
                if len(splitList) != 2 or not splitList[1]:         # Only <nick> and <#>
                    line = wb_cmd(filename, entryNo)                # Call wb_cmd(<nick>, <#>)
                else:
                    line = wb_cmd(filename, entryNo, splitList[1])  # Call wb_cmd(<nick>, <#>, <string>)

    if line is None:
        line = "Not enough stupid things have been said yet."
    return line


# --------------------------------------------------------------------------------
#
# Usage #1:     wb_cmd()
# Result:       Reads a random line from the complete database: wb.txt
# Example:      wb_cmd()
# Output:       [5/34] <SP> Hello World!
#
# Usage #2:     wb_cmd(#)
# Result:       Reads the last line from the complete  database: wb.txt
# Example:      wb_cmd(#)
# Output:       [34/34] <Someone> This is my last test
#
# Usage #3:     wb_cmd(#, <string>)
# Result:       Reads a random line containing <string> from the complete database: wb.txt
# Example:      wb_cmd(#, wbs)
# Output:       [3/7][20/34] <Someone> You have too much fun with WBs
#
# Usage #4:     wb_cmd(<#>)
# Result:       Reads the <#>-th line from the complete database: wb.txt
# Example:      wb_cmd(7)
# Output:       [7/34] <Someone> What should I say here?
#
# Usage #5:     wb_cmd(<#>, <string>)
# Result:       Reads the <#>-th line containing <string> from the complete database: wb.txt
# Example:      wb_cmd(5, wbs)
# Output:       [5/7][22/34] <Someone> I'm starting to think you live to add WBs
#
# Usage #6:     wb_cmd(<nick>)
# Result:       Reads a random line from <nick>.txt
# Example:      wb_cmd(SP)
# Output:       [2/6] <SP> Blarghhhhhh
#
# Usage #7:     wb_cmd(<nick>, #)
# Result:       Reads the last line from <nick>.txt
# Example:      wb_cmd(SP, #)
# Output:       [6/6] <SP> Running out of creativity here
#
# Usage #8:     wb_cmd(<nick>, #, <string>)
# Result:       Reads a random line containing <string> from <nick>.txt
# Example:      wb_cmd(SP, #, one occurrence)
# Output:       [1/1][1/1] <SP> Notice that total count drops due to one occurrence
#
# Usage #9:     wb_cmd(<nick>, <#>)
# Result:       Reads the <#>-th line from <nick>.txt
# Example:      wb_cmd(Someone, 4)
# Output:       [4/5] <Someone> Stop copying everything I say!
#
# Usage #10:    wb_cmd(<nick>, <#>, <string>)
# Result:       Reads the <#>-th line containing <string> from <nick>.txt
# Example:      wb_cmd(SP, 2, so Funny)
# Output:       [2/4][3/6] <SP> Something something so funny
#
# --------------------------------------------------------------------------------
def wb_cmd(param_filename, param_entryNo=None, param_search=None):
    if param_entryNo is None:
        return wb_read(param_filename)
    elif param_search is None:
        return wb_read(param_filename, param_entryNo)
    else:
        return wb_read(param_filename, param_entryNo, param_search)


# ---------------------------------------------------------------------------------
#
# Description:  Reads a <file> and prints out a line. Can specify which line and search terms
# Return:       Formatted line dictating line entry
#
# ---------------------------------------------------------------------------------
def wb_read(param_file, param_count=None, param_key=None):
    if param_key is None:
        result = utility.read_file(param_file, param_count)
        if result is not None:
            line = result[0]
            index = result[1]
            count = result[2]
        else:
            return None
    else:
        result = utility.read_file(param_file, param_count, param_key)
        if result is not None:
            line = result[0]
            index = result[1]
            count = result[2]
            keyindex = result[3]
            keycount = result[4]
        else:
            return None

    # No occurrences of 'param_key' could be found
    if index == -1:
        return line

    if param_key is not None:
        return "[%d/%d][%d/%d] %s" % (index, count, keyindex, keycount, line)

    return "[%d/%d] %s" % (index, count, line)


# ---------------------------------------------------------------------------------
#
# Description:  Just call !wb, used for magic conch mentions
#
# ---------------------------------------------------------------------------------
def ex_with_params(server, nick=None):
    filename = utility.getFile(server, nick)
    return wb_read(filename)


def ex(message):
    return decipher_wb_string(message)
