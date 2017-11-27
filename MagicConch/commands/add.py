import utility
import config
import commands.rem


# ---------------------------------------------------------------------------------
#
# Description:  Help decipher and split up text from the !add trigger
#
# ---------------------------------------------------------------------------------
def decipher_add_string(message):  # param_string = !add <nick> <entry>
    param_string = message.content

    splitList = param_string.split(" ", 2)  # splitList = [!add, <nick>, <entry>]
    if len(splitList) < 3 or not splitList[2]:
        return "Usage: !add <nick> <string>"

    cmd, name, string = splitList
    string = string.strip()
    string = string.replace('\n', ' ')
    string = string.replace('  ', ' ')

    if name == "link":  # !add link <alt-nick> <nick>
        splitList = string.split(" ", 1)  # splitList = [<alt-nick>, <nick+garbage>]

        if len(splitList) != 2 or not splitList[1]:  # no second half
            return "Usage: !add link <alt-nick> <nick>"

        altNick = splitList[0]  # altNick = <alt-nick>
        splitList = splitList[1].split()  # splitList = [<nick>, garbage]
        nick = splitList[0]  # nick = <nick>

        string = altNick + " " + nick  # string = <alt-nick> <nick>

    elif name == "excuse":  # !add excuse <1/2/3> <string>
        splitList = string.split(" ", 1)  # splitList = [<1/2/3>, <string>]
        if splitList[0].isdigit() is False:  # check to make sure is digit
            return "Usage: !add excuse <1:start 2:subject 3:problem> <string>"
        excuseIndex = int(splitList[0])

        if len(splitList) != 2 or not splitList[1] or excuseIndex < 1 or excuseIndex > 3:  # no second half
            return "Usage: !add excuse <1:start 2:subject 3:problem> <string>"

        excuseFiles = ["estart", "esubject", "eproblem"]
        name = excuseFiles[excuseIndex - 1]  # name = <estart/esubject/eproblem>
        string = splitList[1]  # string = <string>

    return addwb_cmd(message.server.name, name, string)  # Call addwb_cmd(<nick>, <string>)


# ---------------------------------------------------------------------------------
#
# Usage:        addwb_cmd(<nick>, <string>, boolean write to master file)
# Result:       Adds <string> to <nick>.txt and WB.txt
#
# ---------------------------------------------------------------------------------
def addwb_cmd(server, param_nick, param_entry):

    doMaster = param_nick not in config.AllSpecialFiles
    if doMaster:
        param_nick = utility.linkcheck(server, param_nick)

    if param_nick in config.SingleEntryFiles:
        # delete file since we are writing new entry
        utility.removeFile(utility.getFile(server, param_nick))
    else:
        # remove before adding to prevent duplicates
        commands.rem.removewb_cmd(server, param_nick, param_entry, doMaster)
    return wb_add(server, param_nick, param_entry, doMaster)


# ---------------------------------------------------------------------------------
#
# Description:  Adds a line from <nick>.txt and wb.txt
# Return:       Success or failure message for adding
#
# ---------------------------------------------------------------------------------
def wb_add(server, param_nick, param_entry, param_doMaster=True):
    masterFile = utility.getFile(server, config.MasterFile[0])
    fileName = utility.getFile(server, param_nick)

    with open(fileName, "a", encoding="utf8") as inputFile, open(masterFile, "a", encoding="utf8") as inputMaster:
        for i in range(3):
            try:
                inputFile.write(param_entry + "\n")
                break
            except OSError:
                print("Error writing to \"%s\"" % fileName)

        if param_doMaster:
            for i in range(3):
                try:
                    inputMaster.write(param_entry + "\n")
                    break
                except OSError:
                    print("Error writing to \"%s\"" % masterFile)

    return "Added to %s: |%s|" % (param_nick, param_entry)


def ex(message):
    return decipher_add_string(message)
