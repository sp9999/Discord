import utility
import config
from datetime import datetime


class CountdownCommand:
    def __init__(self, message):
        self.server = message.server.name
        self.filename = utility.getFile(self.server, config.UtilityFiles[config.UtilityFilesIndex["countdown"]])
        lines = utility.read_all_file(self.filename)
        self.eventNames = []
        self.eventTimes = []
        for line in lines:
            eventName, eventTime = parseLine(line)
            self.eventNames.append(eventName)
            self.eventTimes.append(datetime.fromtimestamp(int(eventTime)))

    def cmd(self):
        return self.countdown()

    def countdown(self):
        finalstring = ""
        eventIt = 0
        for eventTime in self.eventTimes:
            dt = eventTime - datetime.now()
            finalstring += str(eventIt+1) + ") " + self.eventNames[eventIt] + ": "
            if dt.days >= 0:
                # #) <event name>: X days X hours X minutes X seconds until 20YY/MM/DD HH:MM:SS
                finalstring += parseDeltaTime(dt) + " until " + str(eventTime) + "\n"
            else:
                # #) <event name>: date has already passed!
                finalstring += "date has already passed!\n"
            eventIt += 1

        return finalstring


def parseLine(line):
    lastspace = line.rfind(' ')
    eventname = line[:lastspace]
    eventtime = line[lastspace+1:-1]
    return eventname, eventtime


def parseDeltaTime(dt):
    seconds = dt.seconds
    hours = int(seconds / 60 / 60)
    seconds -= (hours * 60 * 60)
    minutes = int(seconds / 60)
    seconds -= minutes * 60
    finalstring = ""
    if dt.days > 0:
        finalstring += str(dt.days) + (" days " if dt.days != 1 else " day ")
    if hours > 0:
        finalstring += str(hours) + (" hours " if hours != 1 else " hour ")
    if minutes > 0:
        finalstring += str(minutes) + (" minutes " if minutes != 1 else " minute ")
    finalstring += str(seconds) + (" seconds" if seconds != 1 else " second")
    return finalstring


def ex(message):
    countdown = CountdownCommand(message)
    return countdown.cmd()
