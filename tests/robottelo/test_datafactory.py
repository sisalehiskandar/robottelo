"""Tests for module ``robottelo.datafactory``."""
import itertools
import six
import unittest2

from robottelo.config import settings
from robottelo.datafactory import (
    generate_strings_list,
    invalid_emails_list,
    invalid_id_list,
    invalid_names_list,
    invalid_values_list,
    InvalidArgumentError,
    valid_data_list,
    valid_emails_list,
    valid_environments_list,
    valid_labels_list,
    valid_names_list,
    valid_usernames_list,
)


class DataCheckTestCase(unittest2.TestCase):
    """Tests for :meth:`robottelo.datafactory.datacheck` decorator"""

    @classmethod
    def setUpClass(cls):
        """Backup the config smoke property"""
        cls.backup = settings.run_one_datapoint

    def test_datacheck_True(self):
        """Tests if run_one_datapoint=false returns all data points"""
        settings.run_one_datapoint = False
        self.assertEqual(len(generate_strings_list()), 7)
        self.assertEqual(len(invalid_id_list()), 4)
        self.assertEqual(len(invalid_emails_list()), 10)
        self.assertEqual(len(invalid_names_list()), 7)
        self.assertEqual(len(invalid_values_list()), 10)
        self.assertEqual(len(valid_labels_list()), 2)
        self.assertEqual(len(valid_data_list()), 7)
        self.assertEqual(len(valid_emails_list()), 8)
        self.assertEqual(len(valid_environments_list()), 3)
        self.assertEqual(len(valid_names_list()), 15)
        self.assertEqual(len(valid_usernames_list()), 4)

    def test_datacheck_False(self):
        """Tests if run_one_datapoint=True returns one data point"""
        settings.run_one_datapoint = True
        self.assertEqual(len(generate_strings_list()), 1)
        self.assertEqual(len(invalid_emails_list()), 1)
        self.assertEqual(len(invalid_id_list()), 1)
        self.assertEqual(len(invalid_names_list()), 1)
        self.assertEqual(len(invalid_values_list()), 1)
        self.assertEqual(len(valid_data_list()), 1)
        self.assertEqual(len(valid_emails_list()), 1)
        self.assertEqual(len(valid_environments_list()), 1)
        self.assertEqual(len(valid_labels_list()), 1)
        self.assertEqual(len(valid_names_list()), 1)
        self.assertEqual(len(valid_usernames_list()), 1)

    @classmethod
    def tearDownClass(cls):
        """Reset the config smoke property"""
        settings.run_one_datapoint = cls.backup


class TestReturnTypes(unittest2.TestCase):
    """Tests for validating return types for different data factory
    functions."""
    def test_return_type(self):
        """This test validates return types for functions:

        1. :meth:`robottelo.datafactory.generate_strings_list`
        2. :meth:`robottelo.datafactory.invalid_emails_list`
        3. :meth:`robottelo.datafactory.invalid_names_list`
        4. :meth:`robottelo.datafactory.valid_data_list`
        5. :meth:`robottelo.datafactory.valid_emails_list`
        6. :meth:`robottelo.datafactory.valid_environments_list`
        7. :meth:`robottelo.datafactory.valid_labels_list`
        8. :meth:`robottelo.datafactory.valid_names_list`
        9. :meth:`robottelo.datafactory.valid_usernames_list`
        10. :meth:`robottelo.datafactory.invalid_id_list`

        """
        for item in itertools.chain(
                generate_strings_list(),
                invalid_emails_list(),
                invalid_names_list(),
                valid_data_list(),
                valid_emails_list(),
                valid_environments_list(),
                valid_labels_list(),
                valid_names_list(),
                valid_usernames_list(),):
            self.assertIsInstance(item, six.text_type)
        for item in invalid_id_list():
            if not (isinstance(item, (six.text_type, int)) or item is None):
                self.fail('Unexpected data type')


class InvalidValuesListTestCase(unittest2.TestCase):
    """Tests for :meth:`robottelo.datafactory.invalid_values_list`"""
    def test_return_values(self):
        """Tests if invalid values list returns right values based on input"""
        # Test valid values
        for value in 'api', 'cli', 'ui', None:
            return_value = invalid_values_list(value)
            self.assertIsInstance(return_value, list)
            if value == 'ui':
                self.assertEqual(len(return_value), 9)
            else:
                self.assertEqual(len(return_value), 10)
        # Test invalid values
        self.assertRaises(InvalidArgumentError, invalid_values_list, ' ')
        self.assertRaises(InvalidArgumentError, invalid_values_list, 'UI')
        self.assertRaises(InvalidArgumentError, invalid_values_list, 'CLI')
        self.assertRaises(InvalidArgumentError, invalid_values_list, 'API')
        self.assertRaises(InvalidArgumentError, invalid_values_list, 'invalid')