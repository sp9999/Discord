import utility
import config


# ---------------------------------------------------------------------------------
#
# Description:  Help decipher and split up text from the !excuse trigger
#
# ---------------------------------------------------------------------------------
def decipher_excuse_string(message):       # param_string = !excuse <#1> <#2> <#2>
    param_string = message.content
    splitList = param_string.split()
    splitCount = len(splitList)
    excuse = None
    startIndex = None
    subjectIndex = None
    problemIndex = None
    server = message.server.name

    if splitCount >= 2:
        startIndex = splitList[1]               # startIndex = <#1>
    if splitCount >= 3:
        subjectIndex = splitList[2]             # subjectIndex = <#2>
    if splitCount >= 4:
        problemIndex = splitList[3]             # problemIndex = <#3>

    if startIndex is None:
        excuse = excuse_cmd(server)                                            # excuse_cmd()
    elif subjectIndex is None:
        excuse = excuse_cmd(server, startIndex)                                # excuse_cmd(<#1>)
    elif problemIndex is None:
        excuse = excuse_cmd(server, startIndex, subjectIndex)                  # excuse_cmd(<#1>, <#2>)
    else:
        excuse = excuse_cmd(server, startIndex, subjectIndex, problemIndex)    # excuse_cmd(<#1>, <#2>, <#3>)

    if excuse is None:
        excuse = "No excuses found. Good work!"
    return excuse


# ---------------------------------------------------------------------------------
#
# Description:  Randomly generate an excuse based off a list of possiblilities
# Return:       An excuse from files estart.txt + esubject.txt + eproblem.txt
#
# ---------------------------------------------------------------------------------
def excuse_cmd(server, startIndex = None, subjectIndex = None, problemIndex = None):
    fileStart = utility.getFile(server, config.ExcuseFiles[0])
    fileSubject = utility.getFile(server, config.ExcuseFiles[1])
    fileProblem = utility.getFile(server, config.ExcuseFiles[2])

    if startIndex == "0":
        startIndex = None
    if subjectIndex == "0":
        subjectIndex = None
    if problemIndex == "0":
        problemIndex = None

    try:
        start, startIndex, startTotal = utility.read_file(fileStart, startIndex)
        subject, subjectIndex, subjectTotal = utility.read_file(fileSubject, subjectIndex)
        problem, problemIndex, problemTotal = utility.read_file(fileProblem, problemIndex)
    except ValueError:
        return "Not all files exist"
    except TypeError:
        return "Not all files exist"

    return "[%d/%d/%d] %s %s %s." %(startIndex, subjectIndex, problemIndex, start, subject, problem)


def ex(message):
    return decipher_excuse_string(message)
