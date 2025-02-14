import unittest
from DataLayer.ddbb_connection import SESSIONMAKER

class RepComun(unittest.TestCase):

    def test_check_connection(self):

        with SESSIONMAKER() as session:
            self.assertTrue(session.is_active)