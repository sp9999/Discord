# secret.py contains sensitive information, below is a list of values used in that file
# BOT_NAME = "Magic Conch"
# BOT_OWNER = "SP"
# Servers = { "Server1", "Server2" }
# DiscordToHexchatMap = { Servers[0]: False, Servers[1]: "C:/Programs/HexChat/config/addons/wb/#Server2/" }
# ServerDefaultTimerChannel = { Servers[0]: "general", Servers[1]: "random"}
# ServerDefaultTimer = { Servers[0]: 0, Servers[1]: 3600 }
# ServerDefaultIgnoreChannels = { Servers[0]: [], Servers[1]: ["general", "techtalk"]}


ExcuseFiles = [
    "estart",
    "esubject",
    "eproblem"
]

SingleEntryFiles = [
    "timer_channel",
    "timer_time",
]

UtilityFilesIndex = {
    "link": 0,
    "whitelist": 1,
    "ignore_channel": 2,
    "timer_channel": 3,
    "timer_time": 4,
    "info": 5,
    "countdown": 6
}

UtilityFiles = [
    "link",
    "whitelist",
    "ignore_channel",
    SingleEntryFiles[0],
    SingleEntryFiles[1],
    "info",
    "countdown",
]

MasterFile = ["wb"]

AllSpecialFiles = ExcuseFiles + UtilityFiles + MasterFile

SEMEN_DEMON = [
    "semen demon",
    "semendemon"
]