import random


class JudgeCommand:
    def __init__(self, message):
        self.minVal = 1
        self.maxVal = 9
        splitList = message.content.split()
        splitCount = len(splitList)

        if splitCount == 2:             # Rand between 1-# or #-1 if 0 or negative
            if splitList[1].isdigit():
                val1 = int(splitList[1])
                if val1 < self.minVal:
                    self.maxVal = self.minVal
                    self.minVal = val1
                else:
                    self.maxVal = val1
        elif splitCount >= 3:          # Rand between min-MAX
            if splitList[1].isdigit() and splitList[2].isdigit():
                val1 = int(splitList[1])
                val2 = int(splitList[2])
                if val1 < val2:
                    self.minVal = val1
                    self.maxVal = val2
                else:
                    self.minVal = val2
                    self.maxVal = val1
            elif splitList[1].isdigit():
                val1 = int(splitList[1])
                if val1 < self.minVal:
                    self.maxVal = self.minVal
                    self.minVal = val1
                else:
                    self.maxVal = val1
            elif splitList[2].isdigit():
                val2 = int(splitList[1])
                if val2 < self.minVal:
                    self.maxVal = self.minVal
                    self.minVal = val2
                else:
                    self.maxVal = val2

    # ---------------------------------------------------------------------------------
    # Usage #1: judge_cmd()
    # Result: Returns number between 1-9
    # Output: [1/9] <random val between 1-9>
    #
    # Usage #2: judge_cmd(<M>)
    # Result: Returns number between 1-M
    # Output: [1/M] <random val between 1-M>
    #
    # Usage #2: judge_cmd(<#, #>)
    # Result: Returns number between #-#
    # Output: [#/#] <random val between #-#>
    # ---------------------------------------------------------------------------------
    def cmd(self):
        return self.judge()

    # ---------------------------------------------------------------------------------
    #
    # Description:  Returns a random number between an interval
    # Return: Min/Max and the random number between the two
    #
    # ---------------------------------------------------------------------------------
    def judge(self):
        rand = random.randint(self.minVal, self.maxVal)
        return "[%d/%d] %d" % (self.minVal, self.maxVal, rand)


def ex(message):
    judge = JudgeCommand(message)
    return judge.cmd()
