import unittest
from unittest.mock import patch, mock_open
import utility
import os


class UtilityTests(unittest.TestCase):

    @patch.object(os, "walk")
    @patch.object(utility, "attemptToGetPath")
    def test_getFilesInPath(self, mock_attemptToGetPath, mock_osWalk):
        path = 'serverName\\'
        mock_attemptToGetPath.return_value = path

        input_files = ("test.txt", "test2.txt", "wb.txt", "invalid")
        mock_osWalk.return_value = [(path, (), input_files)]
        files = utility .getFilesInPath(path)

        assert len(files) == 2
        assert input_files[2][2] not in files
        assert input_files[2][3] not in files


if __name__ == '__main__':
    unittest.main()
