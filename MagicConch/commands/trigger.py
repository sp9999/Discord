import asyncio
import utility
import commands.wb
import secret
import re


class TriggerCommand:
    def __init__(self, server):
        self.server = server
        self.filename = utility.getFile(server, "trigger")
        self.triggers = []

    def load(self):
        self.triggers = utility.read_all_file(self.filename)
        if self.triggers is None:
            return "No triggers found for server [" + self.server + "]"
        else:
            return "Triggers loaded for server [" + self.server + "]"

    def parse(self, message):
        if self.triggers is None:
            return 0, 0

        count = 0
        triggered = []
        for trigger in self.triggers:
            compiled = re.compile("\\b" + trigger[:-1] + "\\b", re.IGNORECASE)
            result = compiled.search(message.content)
            if result is not None:
                triggered.append(result.group(0))
                count += 1

        return triggered, count
