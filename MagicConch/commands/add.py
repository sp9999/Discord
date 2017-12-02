import utility
import config
import secret
import commands.rem


class AddCommand:
    def __init__(self, message):
        self.server = message.server.name
        self.isValid = True
        self.isLink = False
        self.isExcuse = False
        self.doMaster = False

        split_list = message.content.split(" ", 2)  # split_list = [!add, <nick>, <entry>]
        if len(split_list) < 3 or not split_list[2]:
            self.isValid = False
            return

        cmd, self.name, string = split_list
        string = string.strip()
        string = string.replace('\n', ' ')
        self.string = string.replace('  ', ' ')

        if self.name == "link":          # !add link <alt-nick> <nick>
            self.isLink = True

        elif self.name == "excuse":      # !add excuse <1/2/3> <string>
            self.isExcuse = True

    # ---------------------------------------------------------------------------------
    #
    # Description:  Depending on type of add command, return error message with proper usage
    #
    # ---------------------------------------------------------------------------------
    def error(self):
        if self.isLink:
            return "Usage: !add link <alt-nick> <nick>"
        elif self.isExcuse:
            return "Usage: !add excuse <1:start 2:subject 3:problem> <string>"
        else:
            return "Usage: !add <nick> <string>"

    # ---------------------------------------------------------------------------------
    #
    # Description:  Properly sanitize input for !add link
    #
    # ---------------------------------------------------------------------------------
    def link(self):
        split_list = self.string.split(" ", 1)          # splitList = [<alt-nick>, <nick+garbage>]

        if len(split_list) != 2 or not split_list[1]:   # no second half
            self.isValid = False

        alt_nick = split_list[0]                        # alt_nick = <alt-nick>
        split_list = split_list[1].split()              # splitList = [<nick>, garbage]
        nick = split_list[0]                            # nick = <nick>

        self.string = alt_nick + " " + nick             # string = <alt-nick> <nick>

    # ---------------------------------------------------------------------------------
    #
    # Description:  Properly sanitize input for !add excuse
    #
    # ---------------------------------------------------------------------------------
    def excuse(self):
        split_list = self.string.split(" ", 1)          # splitList = [<1/2/3>, <string>]
        if split_list[0].isdigit() is False:            # check to make sure is digit
            self.isValid = False

        excuse_index = int(split_list[0])

        if len(split_list) != 2 or not split_list[1] or excuse_index < 1 or excuse_index > 3:  # no second half
            self.isValid = False

        self.name = config.ExcuseFiles[excuse_index - 1]      # name = <estart/esubject/eproblem>
        self.string = split_list[1]                     # string = <string>

    # ---------------------------------------------------------------------------------
    #
    # Description: Prepares and validates adding of line
    #
    # ---------------------------------------------------------------------------------
    def cmd(self):
        if self.isLink:
            self.link()
        elif self.isExcuse:
            self.excuse()

        if not self.isValid:
            return self.error()

        self.doMaster = self.name not in config.AllSpecialFiles and self.name not in secret.ServerUniqueFiles[self.server]
        if self.doMaster:
            self.name = utility.linkcheck(self.server, self.name)

        if self.name in config.SingleEntryFiles:
            # delete file since we are writing new entry
            utility.removeFile(utility.getFile(self.server, self.name))
        else:
            # remove before adding to prevent duplicates
            commands.rem.wb_remove(self.server, self.name, self.string, self.doMaster)
        return self.add()

    # ---------------------------------------------------------------------------------
    #
    # Description:  Adds a line to <nick>.txt and both wb.txt, info.txt if needed
    # Return:       Success or failure message for adding
    #
    # ---------------------------------------------------------------------------------
    def add(self):
        master_file = utility.getFile(self.server, config.MasterFile[0])
        info_file = utility.getFile(self.server, config.UtilityFiles[5])
        file_name = utility.getFile(self.server, self.name)

        with open(file_name, "a", encoding="utf8") as inputFile, \
                open(master_file, "a", encoding="utf8") as inputMaster, \
                open(info_file, "a", encoding="utf8") as inputInfo:

            for i in range(3):
                try:
                    inputFile.write(self.string + "\n")
                    break
                except OSError:
                    print("Error writing to \"%s\"" % file_name)

            if self.doMaster:
                for i in range(3):
                    try:
                        inputMaster.write(self.string + "\n")
                        break
                    except OSError:
                        print("Error writing to \"%s\"" % master_file)
                for i in range(3):
                    try:
                        inputInfo.write(self.name + "\n")
                        break
                    except OSError:
                        print("Error writing to \"%s\"" % inputFile)

        return "Added to %s: |%s|" % (self.name, self.string)


def ex(message):
    add = AddCommand(message)
    return add.cmd()
