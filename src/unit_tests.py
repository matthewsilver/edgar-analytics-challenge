import sys
import unittest

from src.sessionization import Session

class UnitTests(unittest.TestCase):

    # Error should be thrown if not all 3 filepaths are supplied
    def test_too_few_filepaths(self):
        filepaths = [TIMEOUT_PATH, LOG_PATH, OUTPUT_PATH]
        with self.assertRaises(IndexError) as e:
            p = Session(*filepaths)
        self.assertEqual(str(e.exception), "Please pass all 3 file paths when calling program on command line")


if __name__ == '__main__':
    unittest.main()