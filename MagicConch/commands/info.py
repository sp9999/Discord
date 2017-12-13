import utility
import config
import secret


class InfoCommand:
    def __init__(self, message):
        self.message = message
        self.isValid = True
        self.wbFile = utility.getFile(message.server.name)
        self.infoFile = utility.getFile(message.server.name, config.UtilityFiles[5], False)

        param_string = message.content
        split_list = param_string.split(" ", 1)  # splitList = [!info, <# or build>]
        if len(split_list) == 2:
            self.parameter = split_list[1]

        self.isBuild = self.parameter == "build"
        if self.parameter is '#' or self.parameter.isdigit():
            self.entryNo = self.parameter
        elif not self.isBuild:
            self.isValid = False

    # ---------------------------------------------------------------------------------
    #
    # Description:  Depending on type of add command, return error message with proper usage
    #
    # ---------------------------------------------------------------------------------
    def error(self):
        if self.isBuild:
            return "Usage: !info build", None
        else:
            return "Usage: !info <#>", None

    # --------------------------------------------------------------------------------
    #
    # Usage:        read(#)
    # Result:       Reads a line from the complete database: wb.txt and info.txt in order to find owner of line
    # Example:      read(#)
    # Output:       [SP] <SP> Hello World!
    #
    # --------------------------------------------------------------------------------
    def read(self):
        wb_text = utility.read_file(self.wbFile, self.entryNo)
        info_text = utility.read_file(self.infoFile, self.entryNo)

        if info_text is not None and wb_text is not None:
            return "[%s]" % info_text[0], "%s" % wb_text[0]
        return "No information on this line", None

    # --------------------------------------------------------------------------------
    #
    # Usage:        build()
    # Result:       Creates info.txt by reading wb.txt and every file in directory to find owner of each line
    # Example:      build()
    # Output:       None
    #
    # --------------------------------------------------------------------------------
    def build(self):
        files = utility.getFilesInPath(self.message.server.name)
        path = utility.attemptToGetPath(self.message.server.name)
        # Open wb file and store lines
        with open(self.infoFile, "w", encoding="utf8") as infoFp:
            with open(self.wbFile, encoding="utf8") as wbFp:

                # iterate over each line in wb.txt
                for line in wbFp:
                    found = False
                    owner = ""

                    # iterate through each file in path
                    for ownerFile in files:
                        if utility.isLineInFile(path+ownerFile, line):
                            found = True
                            owner = ownerFile.split(".", 1)[0]
                            break

                    if not found:
                        owner = "Missing owner"

                    for i in range(3):
                        try:
                            infoFp.write(owner + "\n")
                            break
                        except OSError:
                            print("Error writing to \"%s\"" % self.infoFile)

    # --------------------------------------------------------------------------------
    #
    # Usage:        cmd(#/build)
    # Result:       Determines whether info.read or info.build function should get called
    # Example:      cmd(#) or cmd(build)
    #
    # --------------------------------------------------------------------------------
    def cmd(self):
        if not self.isValid:
            return self.error()

        line = ""
        if self.isBuild:
            if self.message.author.name == secret.BOT_OWNER:
                self.build()
                line = "Info compiled successfully", None
        else:
            line = self.read()

        return line


def ex(message):
    info = InfoCommand(message)
    return info.cmd()
