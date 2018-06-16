import unittest
from unittest.mock import patch
from types import SimpleNamespace
import commands.judge
import random


class JudgeTests(unittest.TestCase):

    @patch.object(random, "randint")
    def test_judgeCommand_standard(self, mock_randint):
        mock_randint.return_value = 9
        input = SimpleNamespace(content='!judge')
        output = commands.judge.ex(input)

        assert output == "[1/9] 9"

    @patch.object(random, "randint")
    def test_judgeCommand_singleparam_lowermax(self, mock_randint):
        mock_randint.return_value = 5
        input = SimpleNamespace(content='!judge 5')
        output = commands.judge.ex(input)

        assert output == "[1/5] 5"

    @patch.object(random, "randint")
    def test_judgeCommand_singleparam_lowermin(self, mock_randint):
        mock_randint.return_value = 1
        input = SimpleNamespace(content='!judge 0')
        output = commands.judge.ex(input)

        assert output == "[0/1] 1"

    @patch.object(random, "randint")
    def test_judgeCommand_singleparam_highermax(self, mock_randint):
        mock_randint.return_value = 20
        input = SimpleNamespace(content='!judge 20')
        output = commands.judge.ex(input)

        assert output == "[1/20] 20"

    @patch.object(random, "randint")
    def test_judgeCommand_singleparam_invalid(self, mock_randint):
        mock_randint.return_value = 9
        input = SimpleNamespace(content='!judge test')
        output = commands.judge.ex(input)

        assert output == "[1/9] 9"

    @patch.object(random, "randint")
    def test_judgeCommand_twoparam_lowthenhigh(self, mock_randint):
        mock_randint.return_value = 3
        input = SimpleNamespace(content='!judge 0 5')
        output = commands.judge.ex(input)

        assert output == "[0/5] 3"

    @patch.object(random, "randint")
    def test_judgeCommand_twoparam_highthenlow(self, mock_randint):
        mock_randint.return_value = 1
        input = SimpleNamespace(content='!judge 20 1')
        output = commands.judge.ex(input)

        assert output == "[1/20] 1"

    @patch.object(random, "randint")
    def test_judgeCommand_twoparam_same(self, mock_randint):
        mock_randint.return_value = 5
        input = SimpleNamespace(content='!judge 5 5')
        output = commands.judge.ex(input)

        assert output == "[5/5] 5"

    @patch.object(random, "randint")
    def test_judgeCommand_twoparam_invalidthenval(self, mock_randint):
        mock_randint.return_value = 5
        input = SimpleNamespace(content='!judge test 5')
        output = commands.judge.ex(input)

        assert output == "[1/5] 5"

    @patch.object(random, "randint")
    def test_judgeCommand_twoparam_invalidthenval(self, mock_randint):
        mock_randint.return_value = 5
        input = SimpleNamespace(content='!judge 5 invalid')
        output = commands.judge.ex(input)

        assert output == "[1/5] 5"

    @patch.object(random, "randint")
    def test_judgeCommand_threeparam(self, mock_randint):
        mock_randint.return_value = 3
        input = SimpleNamespace(content='!judge 0 5 50')
        output = commands.judge.ex(input)

        assert output == "[0/5] 3"


if __name__ == '__main__':
    unittest.main()
