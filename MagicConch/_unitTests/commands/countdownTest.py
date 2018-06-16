import unittest
from unittest.mock import patch
from types import SimpleNamespace
import commands.countdown
import utility
import time
from datetime import datetime
from datetime import timedelta


class CountdownTests(unittest.TestCase):

    @patch.object(utility, "read_all_file")
    def test_countdownCommand_multiple_days(self, mock_read_all_file):
        futureevent = datetime.now() + timedelta(days=3)
        lines = {
            "future event " + str(int(time.mktime(futureevent.timetuple()))) + "\n"
        }
        mock_read_all_file.return_value = lines
        serverInput = SimpleNamespace(name="test")
        input = SimpleNamespace(content='!countdown', server=serverInput)
        output = commands.countdown.ex(input)

        assert output.startswith("1) future event: 2 days")

    @patch.object(utility, "read_all_file")
    def test_countdownCommand_single_days(self, mock_read_all_file):
        futureevent = datetime.now() + timedelta(days=2)
        lines = {
            "future event " + str(int(time.mktime(futureevent.timetuple()))) + "\n"
        }
        mock_read_all_file.return_value = lines
        serverInput = SimpleNamespace(name="test")
        input = SimpleNamespace(content='!countdown', server=serverInput)
        output = commands.countdown.ex(input)

        assert output.startswith("1) future event: 1 day")

    @patch.object(utility, "read_all_file")
    def test_countdownCommand_multiple_hours(self, mock_read_all_file):
        futureevent = datetime.now() + timedelta(days=1)
        lines = {
            "future event " + str(int(time.mktime(futureevent.timetuple()))) + "\n"
        }
        mock_read_all_file.return_value = lines
        serverInput = SimpleNamespace(name="test")
        input = SimpleNamespace(content='!countdown', server=serverInput)
        output = commands.countdown.ex(input)

        assert output.startswith("1) future event: 23 hours")

    @patch.object(utility, "read_all_file")
    def test_countdownCommand_single_hours(self, mock_read_all_file):
        futureevent = datetime.now() + timedelta(hours=2)
        lines = {
            "future event " + str(int(time.mktime(futureevent.timetuple()))) + "\n"
        }
        mock_read_all_file.return_value = lines
        serverInput = SimpleNamespace(name="test")
        input = SimpleNamespace(content='!countdown', server=serverInput)
        output = commands.countdown.ex(input)

        assert output.startswith("1) future event: 1 hour")

    @patch.object(utility, "read_all_file")
    def test_countdownCommand_multiple_minutes(self, mock_read_all_file):
        futureevent = datetime.now() + timedelta(hours=1)
        lines = {
            "future event " + str(int(time.mktime(futureevent.timetuple()))) + "\n"
        }
        mock_read_all_file.return_value = lines
        serverInput = SimpleNamespace(name="test")
        input = SimpleNamespace(content='!countdown', server=serverInput)
        output = commands.countdown.ex(input)

        assert output.startswith("1) future event: 59 minutes")

    @patch.object(utility, "read_all_file")
    def test_countdownCommand_single_minute(self, mock_read_all_file):
        futureevent = datetime.now() + timedelta(minutes=2)
        lines = {
            "future event " + str(int(time.mktime(futureevent.timetuple()))) + "\n"
        }
        mock_read_all_file.return_value = lines
        serverInput = SimpleNamespace(name="test")
        input = SimpleNamespace(content='!countdown', server=serverInput)
        output = commands.countdown.ex(input)

        assert output.startswith("1) future event: 1 minute")

    @patch.object(utility, "read_all_file")
    def test_countdownCommand_multiple_seconds(self, mock_read_all_file):
        futureevent = datetime.now() + timedelta(minutes=1)
        lines = {
            "future event " + str(int(time.mktime(futureevent.timetuple()))) + "\n"
        }
        mock_read_all_file.return_value = lines
        serverInput = SimpleNamespace(name="test")
        input = SimpleNamespace(content='!countdown', server=serverInput)
        output = commands.countdown.ex(input)

        assert output.startswith("1) future event: 59 seconds")

    @patch.object(utility, "read_all_file")
    def test_countdownCommand_single_second(self, mock_read_all_file):
        futureevent = datetime.now() + timedelta(seconds=2)
        lines = {
            "future event " + str(int(time.mktime(futureevent.timetuple()))) + "\n"
        }
        mock_read_all_file.return_value = lines
        serverInput = SimpleNamespace(name="test")
        input = SimpleNamespace(content='!countdown', server=serverInput)
        output = commands.countdown.ex(input)

        assert output.startswith("1) future event: 1 second")

    @patch.object(utility, "read_all_file")
    def test_countdownCommand_past(self, mock_read_all_file):
        pastevent = datetime.now() + timedelta(seconds=-1)
        lines = {
            "past event " + str(int(time.mktime(pastevent.timetuple()))) + "\n"
        }
        mock_read_all_file.return_value = lines
        serverInput = SimpleNamespace(name="test")
        input = SimpleNamespace(content='!countdown', server=serverInput)
        output = commands.countdown.ex(input)

        assert output.startswith("1) past event: date has already passed!")

    @patch.object(utility, "read_all_file")
    def test_countdownCommand_multiple(self, mock_read_all_file):
        futureevent = datetime.now() + timedelta(hours=2)
        pastevent = datetime.now() + timedelta(seconds=-1)
        lines = [
            "future event " + str(int(time.mktime(futureevent.timetuple()))) + "\n",
            "past event " + str(int(time.mktime(pastevent.timetuple()))) + "\n"
        ]
        mock_read_all_file.return_value = lines
        serverInput = SimpleNamespace(name="test")
        input = SimpleNamespace(content='!countdown', server=serverInput)
        output = commands.countdown.ex(input)

        assert output.find("1) future event: 1 hour") != -1 and output.find("2) past event: date has already passed!") != -1
