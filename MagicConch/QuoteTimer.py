import asyncio
import utility
import commands.wb
import secret


class QuoteTimer:
    def __init__(self, client, server):
        self.client = client
        self.server = server
        self.channel = utility.getServerTimerChannel(server)
        self.timer = utility.getServerTimer(server.name)
        self.loop = asyncio.get_event_loop()

    def setup(self):
        self.startTimer()
        print("Set up QuoteTimer for " + self.server.name + " in #" + self.channel.name +
              " with a " + str(self.timer) + " second interval")

    def startTimer(self):
        self.timer = utility.getServerTimer(self.server.name)
        self.loop.create_task(self.periodicWB())

    async def periodicWB(self):
        sleep_timer = self.timer
        if self.timer == 0:
            sleep_timer = 600
        await asyncio.sleep(sleep_timer)

        if self.timer != 0:
            string = commands.wb.ex_with_params(self.server.name)
            if string:
                channel = utility.getServerTimerChannel(self.server)
                if channel is not None:
                    skip = False
                    async for msg in self.client.logs_from(channel, limit=10):
                        if msg.author.name == secret.BOT_NAME:
                            skip = True
                            break
                    if not skip:
                        await self.client.send_message(channel, utility.textBlock(string))
        self.startTimer()

