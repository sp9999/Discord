import utility
import config
import secret

class RemCommand:
    def __init__(self, message):
        self.server = message.server.name
        self.isValid = True
        self.isExcuse = False
        self.doMaster = False

        split_list = message.content.split(" ", 2)
        if len(split_list) != 3 or not split_list[2]:
            self.isValid = False
            return

        cmd, self.name, string = split_list
        string = string.strip()
        string = string.replace('\n', ' ')
        self.string = string.replace('  ', ' ')

        if self.name == "wb":
            self.isValid = False
            return

        if self.name == "excuse":  # !rem excuse <1/2/3> <string>
            self.isExcuse = True

    # ---------------------------------------------------------------------------------
    #
    # Description:  Depending on type of rem command, return error message with proper usage
    #
    # ---------------------------------------------------------------------------------
    def error(self):
        if self.isExcuse:
            return "Usage: !rem excuse <1:start 2:subject 3:problem> <entry# or string>"
        else:
            return "Usage: !rem <nick> <entry# or string>"

    # ---------------------------------------------------------------------------------
    #
    # Description:  Properly sanitize input for !rem excuse
    #
    # ---------------------------------------------------------------------------------
    def excuse(self):
        split_list = self.string.split(" ", 1)  # splitList = [<1/2/3>, <string>]
        if split_list[0].isdigit() is False:  # check to make sure is digit
            self.isValid = False

        excuse_index = int(split_list[0])

        if len(split_list) != 2 or not split_list[1] or excuse_index < 1 or excuse_index > 3:  # no second half
            self.isValid = False

        self.name = config.ExcuseFiles[excuse_index - 1]  # name = <estart/esubject/eproblem>
        self.string = split_list[1]  # string = <string>

    # ---------------------------------------------------------------------------------
    #
    # Description: Prepares and validates removing of line
    #
    # ---------------------------------------------------------------------------------
    def cmd(self):
        if self.isExcuse:
            self.excuse()

        if not self.isValid:
            return self.error()

        self.doMaster = self.name not in config.AllSpecialFiles and self.name not in secret.ServerUniqueFiles[self.server]
        if self.doMaster:
            self.name = utility.linkcheck(self.server, self.name)

        return self.rem()

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
    def rem(self):
        line = wb_remove(self.server, self.name, self.string, self.doMaster)

        if line is None:
            return "File %s does not exist" % self.name

        if self.string == '#':
            if len(line) > 0:
                return "Removing last entry from %s: |%s|" % (self.name, line)
            else:
                return "No entries exist for %s." % self.name
        elif self.string.isdigit():
            if len(line) > 0:
                return "Removing line number %d from %s: |%s|" % (int(self.string), self.name, line)
            else:
                return "Entry number %d does not exist." % int(self.string)
        else:
            if line and len(line) > 0:
                return "Removing line from %s: |%s|" % (self.name, line)
            else:
                return "Line does not exist in %s. Already removed!" % self.name


# ---------------------------------------------------------------------------------
#
# Description:  Removes a line from <nick>.txt. Can specify which line and search terms
# Return:       Removed line
# Note:         Public function since add requires ability to remove lines
#
# ---------------------------------------------------------------------------------
def wb_remove(server, param_nick, param_entry, param_do_master):
    master_file = utility.getFile(server, config.MasterFile[0])
    info_file = utility.getFile(server, config.UtilityFiles[5])
    file_name = utility.getFile(server, param_nick)
    temp_file = utility.getFile(server, "temp")

    remove_line = None
    remove_last_line = False
    remove_line_no = None

    if param_entry == '#':
        remove_last_line = True
    elif param_entry.isdigit():
        remove_line_no = int(param_entry)
    else:
        remove_line = param_entry

    master_line, master_line_no = utility.remove(file_name, temp_file, remove_last_line, remove_line_no, remove_line)
    if not master_line:
        return "File not found"

    if param_do_master:
        master_line, master_line_no = utility.remove(master_file, temp_file, None, None, master_line)
        utility.remove(info_file, temp_file, None, master_line_no)

    return master_line


def ex(message):
    rem = RemCommand(message)
    return rem.cmd()
