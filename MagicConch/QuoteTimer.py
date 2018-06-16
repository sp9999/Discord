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
        print("QuoteTimer " + self.server.name + " in #" + self.channel.name +
              ": start periodicWB")
        await self.client.wait_until_ready()
        sleep_timer = self.timer
        if self.timer == 0:
            sleep_timer = 600
            print("QuoteTimer " + self.server.name + " in #" + self.channel.name +
                  ": start sleep")
        await asyncio.sleep(sleep_timer)
        print("QuoteTimer " + self.server.name + " in #" + self.channel.name +
              ": end sleep")

        if self.timer != 0:
            print("QuoteTimer " + self.server.name + " in #" + self.channel.name +
                  ": Getting quote")
            number_string, line = commands.wb.ex_with_params(self.server.name)
            print("QuoteTimer " + self.server.name + " in #" + self.channel.name +
                  ": Quote got")
            if number_string:
                print("QuoteTimer " + self.server.name + " in #" + self.channel.name +
                      ": Getting channel")
                channel = utility.getServerTimerChannel(self.server)
                print("QuoteTimer " + self.server.name + " in #" + self.channel.name +
                      ": Channel got")
                if channel is not None:
                    skip = False
                    print("QuoteTimer " + self.server.name + " in #" + self.channel.name +
                          ": Getting logs")
                    async for msg in self.client.logs_from(channel, limit=10):
                        if msg.author.name == secret.BOT_NAME:
                            skip = True
                            break
                    print("QuoteTimer " + self.server.name + " in #" + self.channel.name +
                          ": Logs got")
                    if not skip:
                        print("QuoteTimer " + self.server.name + " in #" + self.channel.name +
                              ": Sending message")
                        await self.client.send_message(channel, utility.wbBlock(number_string, line))
                        print("QuoteTimer " + self.server.name + " in #" + self.channel.name +
                              ": Message sent")
        self.startTimer()

