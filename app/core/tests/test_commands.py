"""
test custom Django management commands
"""

from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

# the decorator : the command to be mocking the database
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """test waiting for db if database ready"""
        patched_check.return_value = True

        # if setup correctly the command can be called
        call_command('wait_for_db')

        # asserts the mocked object is called
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self,patched_sleep,patched_check):
        """test waiting for db when getting OperationalError"""

        # after trial and error we know that roughly we can find 
        # this number of errors.

        # side_effect to validate if errors have been raised
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        # should have been called 6 times, each time defined in side_effect
        self.assertEqual(patched_check.call_count, 6)

        # makes sure base parameters are defined
        patched_check.assert_called_with(databases=['default'])


        