import utility


class WBCommand:
    def __init__(self, message):
        self.server = message.server.name
        self.hasEntryNo = False
        self.hasSearch = False
        self.entryNo = None
        self.nick = "Global"
        self.filename = utility.getFile(self.server)

        split_list = message.content.split(" ", 1)  # splitList = [!wb, <nick> <#> <string>]

        if len(split_list) == 2 and split_list[1]:  # No other parameters
            split_list = split_list[1].split(" ", 1)              # splitList = [<nick>, <#> <string>]
            if split_list[0] is '#' or split_list[0].isdigit():   # in instance of [<#>, <string>]
                self.entryNo = split_list[0]                     # entryNo = <#>
                self.hasEntryNo = True
                if len(split_list) == 2 and split_list[1]:
                    self.search = split_list[1]
                    self.hasSearch = True
            else:
                self.nick = split_list[0]                        # nick = <nick>
                self.filename = utility.getFile(message.server.name, self.nick)
                if len(split_list) == 2 and split_list[1]:        # more parameters exist
                    split_list = split_list[1].split(" ", 1)      # splitList = [<#>, <string>]
                    self.entryNo = split_list[0]
                    self.hasEntryNo = True

                    if len(split_list) == 2 and split_list[1]:  # search param exists
                        self.search = split_list[1]
                        self.hasSearch = True




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
    def cmd(self):
        return self.wb()

    # ---------------------------------------------------------------------------------
    #
    # Description:  Reads a <file> and prints out a line. Can specify which line and search terms
    # Return:       Line entry, line, and other information
    #
    # ---------------------------------------------------------------------------------
    def wb(self):
        if not self.hasSearch:
            result = utility.read_file(self.filename, self.entryNo)
            if result is not None:
                line = result[0]
                index = result[1]
                count = result[2]
            else:
                return "Not enough stupid things have been said yet.", None
        else:
            result = utility.read_file(self.filename, self.entryNo, self.search)
            if result is not None:
                line = result[0]
                index = result[1]
                count = result[2]
                keyindex = result[3]
                keycount = result[4]
            else:
                return "Not enough stupid things have been said yet.", None

                # No occurrences of 'param_key' could be found
        if index == -1:
            return line, None

        if self.hasSearch:
            return "[%d/%d][%d/%d]" % (index, count, keyindex, keycount), "%s" % line

        return "[%d/%d]" % (index, count), "%s" % line


def wb_global(server_filename):
    result = utility.read_file(server_filename)
    if result is not None:
        line = result[0]
        index = result[1]
        count = result[2]

    return "[%d/%d]" % (index, count), "%s" % line


# ---------------------------------------------------------------------------------
#
# Description:  Just call !wb, used for magic conch mentions
#
# ---------------------------------------------------------------------------------
def ex_with_params(server, nick=None):
    filename = utility.getFile(server, nick)
    return wb_global(filename)


def ex(message):
    wb = WBCommand(message)
    return wb.cmd()
