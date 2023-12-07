import sys
import os

# Add the path to your project's root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Package Module Imports
import unittest
from unittest.mock import patch
from io import StringIO
import time
# Project Module Imports
from main import UserMenu
from output_messages import output_messages as output
from factory_classes import ConfigFileFactory, CampaignFactory
from object_classes import Campaign




# Tests only work with an empty game_configs dir
class EditorBBTests(unittest.TestCase):
    # 
    CAMPAIGN_NAME_VALID_MIN = 'A'
    CAMPAIGN_NAME_VALID_LOWER = 'Qagzaoyveehtomoowwehdeu'
    CAMPAIGN_NAME_VALID_NOMINAL = 'Eesyaepuontaodgeavaiboerulheigniutedmepmeotehertucaamsamenhiohse'
    CAMPAIGN_NAME_VALID_UPPER = ('Soehxefinegauyiogdaraejounoazeoqoztacseoyditzeeckiekroctodereav'
        + 'aatmadtaekyeihxeutaapzeamozeseeqrahne')
    CAMPAIGN_NAME_VALID_MAX = ('Qeathainlawcainxarhiteapheerlehwemaetfibosutoanmizeyhaahmaodohseta'
        + 'nyahnogiehsoyyeurelvoceaherevoiclotpaesihtenrumonivethuhjoe')
    CAMPAIGN_NAME_INVALID_MAX = ('Saaneniotordatawwaariehwehohuazeyajietaavoiseinhiohtitdeetiqauyu'
        + 'etatognualseokoseatciindeejaoheuhaumaameofuotseewhoseohtoephao')
    
    CAMPAIGN_NAME_INVALID_MIN_ALL_SPEC = '/'
    CAMPAIGN_NAME_INVALID_LOWER_ALL_SPEC = '*/'
    CAMPAIGN_NAME_INVALID_NOMINAL_ALL_SPEC = ('*?)()_(^$$^&*(?*/*/))*/}/*/*//*/*???<<<><'
        + ':""?"::::":><>*&$&#%@%@')
    CAMPAIGN_NAME_INVALID_UPPER_ALL_SPEC = ('*?)()_(^$$^&*(?*/*/))*/}/*/*//*/*???<<<><:"' 
        + '"?"::::":><>*&$&#%@%@&*(?*/*/))*<</*/*//>/*???<<<><:*?)()_(')
    CAMPAIGN_NAME_INVALID_MAX_ALL_SPEC = ('*?)()_(^$$^&*(?*/*/))*/}/*/*//*/*???<<<><:""?"::::":><>*&$&#%@%@'
        + '*?)()_(^$$^&*(?*/*/))*/}//*//**???<<><:""?"::::":><>*&$&#%@%@')

    @classmethod
    def setUpClass(cls):
        # Code to set up resources before all tests in this class
        cls._menu = UserMenu()
        cls._file_name = "unittest"
        cls._extension = '.bin'
        cls._configs_path = "game_configs"
        cls._file_manager = ConfigFileFactory()
        cls._campaign = Campaign("unittest")

    @classmethod
    def tearDownClass(cls):
        # Code to clean up resources after all tests in this class
        for filename in os.listdir(cls._configs_path):
            if (filename != ".gitkeep"):
                file_path = os.path.join(cls._configs_path, filename)
                os.remove(file_path)

    @patch('builtins.input', side_effect=['1', CAMPAIGN_NAME_VALID_MIN, '9', '2', '3'])
    def test_create_campaign_valid_boundary_value_min(self, _):
        EditorBBTests.tearDownClass()
        file_path = os.path.join(self._configs_path, self.CAMPAIGN_NAME_VALID_MIN + 
                                 EditorBBTests._extension)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_output:
            self._menu.display_editor_menu()
        self.assertTrue(os.path.isfile(file_path))
        
    @patch('builtins.input', side_effect=['1', CAMPAIGN_NAME_VALID_LOWER, '9', '2', '3'])
    def test_create_campaign_valid_boundary_value_lower(self, _):
        EditorBBTests.tearDownClass()   
        file_path = os.path.join(self._configs_path, self.CAMPAIGN_NAME_VALID_LOWER + 
                                 EditorBBTests._extension)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_output:
            self._menu.display_editor_menu()
        self.assertTrue(os.path.isfile(file_path))

    @patch('builtins.input', side_effect=['1', CAMPAIGN_NAME_VALID_NOMINAL, '9', '2', '3'])
    def test_create_campaign_valid_boundary_value_nominal(self, _):
        EditorBBTests.tearDownClass()
        file_path = os.path.join(self._configs_path, self.CAMPAIGN_NAME_VALID_NOMINAL + 
                                 EditorBBTests._extension)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_output:
            self._menu.display_editor_menu()
        self.assertTrue(os.path.isfile(file_path))

    @patch('builtins.input', side_effect=['1', CAMPAIGN_NAME_VALID_UPPER, '9', '2', '3'])
    def test_create_campaign_valid_boundary_value_upper(self, _):
        EditorBBTests.tearDownClass()
        file_path = os.path.join(self._configs_path, self.CAMPAIGN_NAME_VALID_UPPER + 
                                 EditorBBTests._extension)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_output:
            self._menu.display_editor_menu()
        self.assertTrue(os.path.isfile(file_path))

    @patch('builtins.input', side_effect=['1', CAMPAIGN_NAME_VALID_MAX, '9', '2', '3'])
    def test_create_campaign_valid_boundary_value_max(self, _):
        EditorBBTests.tearDownClass()
        file_path = os.path.join(self._configs_path, self.CAMPAIGN_NAME_VALID_MAX + 
                                 EditorBBTests._extension)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_output:
            self._menu.display_editor_menu()
        self.assertTrue(os.path.isfile(file_path))

    @patch('builtins.input', side_effect=['1', '', 'back', '3'])
    def test_create_campaign_invalid_boundary_value_min(self, _):
        EditorBBTests.tearDownClass()
        file_path = os.path.join(self._configs_path, EditorBBTests._extension)
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.display_editor_menu()

        actual_output = mock_stdout.getvalue().strip()
        expected_output = (output.campaign_editor_choices() + '\n' +
            output.input_less_min_length(CampaignFactory.CAMPAIGN_NAME_LEN_MIN) + 
            '\n' + output.campaign_editor_choices())
        self.assertEqual(actual_output, expected_output)
        self.assertFalse(os.path.isfile(file_path))

    @patch('builtins.input', side_effect=['1', CAMPAIGN_NAME_INVALID_MAX, 'back', '3'])
    def test_create_campaign_invalid_boundary_value_max(self, _):
        EditorBBTests.tearDownClass()
        file_path = os.path.join(self._configs_path, self.CAMPAIGN_NAME_INVALID_MAX + 
                                 EditorBBTests._extension)
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.display_editor_menu()

        actual_output = mock_stdout.getvalue().strip()
        expected_output = (output.campaign_editor_choices() + '\n' +
            output.input_exceeds_max_length(CampaignFactory.CAMPAIGN_NAME_LEN_MAX) + 
            '\n' + output.campaign_editor_choices())
        self.assertEqual(actual_output, expected_output)
        self.assertFalse(os.path.isfile(file_path))

    @patch('builtins.input', side_effect=['1', CAMPAIGN_NAME_INVALID_MIN_ALL_SPEC, 'back', '3'])
    def test_create_campaign_invalid_spec_chars_boundary_value_min(self, _):
        EditorBBTests.tearDownClass()
        file_path = os.path.join(self._configs_path, self.CAMPAIGN_NAME_INVALID_MIN_ALL_SPEC + 
                                 EditorBBTests._extension)
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.display_editor_menu()

        actual_output = mock_stdout.getvalue().strip()
        expected_output = (output.campaign_editor_choices() + '\n' +
            output.invalid_chars_campaign_name(self.CAMPAIGN_NAME_INVALID_MIN_ALL_SPEC) + 
            '\n' + output.campaign_editor_choices())
        self.assertEqual(actual_output, expected_output)
        self.assertFalse(os.path.isfile(file_path))

    @patch('builtins.input', side_effect=['1', CAMPAIGN_NAME_INVALID_LOWER_ALL_SPEC, 'back', '3'])
    def test_create_campaign_invalid_spec_chars_boundary_value_lower(self, _):
        EditorBBTests.tearDownClass()
        file_path = os.path.join(self._configs_path, self.CAMPAIGN_NAME_INVALID_LOWER_ALL_SPEC + 
                                 EditorBBTests._extension)
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.display_editor_menu()

        actual_output = mock_stdout.getvalue().strip()
        expected_output = (output.campaign_editor_choices() + '\n' +
            output.invalid_chars_campaign_name(self.CAMPAIGN_NAME_INVALID_LOWER_ALL_SPEC) + 
            '\n' + output.campaign_editor_choices())
        self.assertEqual(actual_output, expected_output)
        self.assertFalse(os.path.isfile(file_path))

    @patch('builtins.input', side_effect=['1', CAMPAIGN_NAME_INVALID_NOMINAL_ALL_SPEC, 'back',
                                           '3'])
    def test_create_campaign_invalid_spec_chars_boundary_value_nominal(self, _):
        EditorBBTests.tearDownClass()
        file_path = os.path.join(self._configs_path, self.CAMPAIGN_NAME_INVALID_NOMINAL_ALL_SPEC + 
                                 EditorBBTests._extension)
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.display_editor_menu()

        actual_output = mock_stdout.getvalue().strip()
        expected_output = (output.campaign_editor_choices() + '\n' +
            output.invalid_chars_campaign_name(self.CAMPAIGN_NAME_INVALID_NOMINAL_ALL_SPEC) + 
            '\n' + output.campaign_editor_choices())
        self.assertEqual(actual_output, expected_output)
        self.assertFalse(os.path.isfile(file_path))

    @patch('builtins.input', side_effect=['1', CAMPAIGN_NAME_INVALID_UPPER_ALL_SPEC, 'back', '3'])
    def test_create_campaign_invalid_spec_chars_boundary_value_upper(self, _):
        EditorBBTests.tearDownClass()
        file_path = os.path.join(self._configs_path, self.CAMPAIGN_NAME_INVALID_UPPER_ALL_SPEC + 
                                 EditorBBTests._extension)
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.display_editor_menu()

        actual_output = mock_stdout.getvalue().strip()
        expected_output = (output.campaign_editor_choices() + '\n' +
            output.invalid_chars_campaign_name(self.CAMPAIGN_NAME_INVALID_UPPER_ALL_SPEC) + 
            '\n' + output.campaign_editor_choices())
        self.assertEqual(actual_output, expected_output)
        self.assertFalse(os.path.isfile(file_path))

    @patch('builtins.input', side_effect=['1', CAMPAIGN_NAME_INVALID_MAX_ALL_SPEC, 'back', '3'])
    def test_create_campaign_invalid_spec_chars_boundary_value_max(self, _):
        EditorBBTests.tearDownClass()
        file_path = os.path.join(self._configs_path, self.CAMPAIGN_NAME_INVALID_MAX_ALL_SPEC + 
                                 EditorBBTests._extension)
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.display_editor_menu()

        actual_output = mock_stdout.getvalue().strip()
        expected_output = (output.campaign_editor_choices() + '\n' +
            output.invalid_chars_campaign_name(self.CAMPAIGN_NAME_INVALID_MAX_ALL_SPEC) + 
            '\n' + output.campaign_editor_choices())
        self.assertEqual(actual_output, expected_output)
        self.assertFalse(os.path.isfile(file_path))

    @patch('builtins.input', side_effect=['1', 'unittest', 'back', '3'])
    def test_create_campaign_invalid_duplicate_name(self, _):
        # Creates file to delete for test
        file_path = os.path.join(self._configs_path, self._file_name + self._extension)
        if not os.path.isfile(file_path):
            self._file_manager.create_config_file(self._campaign)

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.display_editor_menu()

        actual_output = mock_stdout.getvalue().strip()
        expected_output = (output.campaign_editor_choices() + '\n' +
            output.filename_exists(self._file_name) + '\n' + output.campaign_editor_choices())
        self.assertEqual(actual_output, expected_output)
        self.assertTrue(os.path.isfile(file_path))

    @patch('builtins.input', side_effect=['1', 'UNITTEST', 'back', '3'])
    def test_create_campaign_invalid_duplicate_name_case_sensitive(self, _):
        # Creates file to delete for test
        file_path = os.path.join(self._configs_path, self._file_name + 
                                 self._extension)
        if not os.path.isfile(file_path):
            self._file_manager.create_config_file(self._campaign)

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.display_editor_menu()

        actual_output = mock_stdout.getvalue().strip()
        expected_output = (output.campaign_editor_choices() + '\n' +
            output.filename_exists(self._file_name.upper()) + '\n' + 
            output.campaign_editor_choices())
        self.assertEqual(actual_output, expected_output)
        self.assertTrue(os.path.isfile(file_path))

    @patch('builtins.input', side_effect=['1', 'back', '3'])
    def test_create_campaign_valid_back_prompt(self, _):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.display_editor_menu()

        actual_output = mock_stdout.getvalue().strip()
        expected_output = (output.campaign_editor_choices() + '\n' 
                           + output.campaign_editor_choices())
        self.assertEqual(actual_output, expected_output)

    @patch('builtins.input', side_effect=['1', 'BACK', '3'])
    def test_create_campaign_valid_back_prompt_case_max(self, _):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.display_editor_menu()

        actual_output = mock_stdout.getvalue().strip()
        expected_output = (output.campaign_editor_choices() + '\n' 
                           + output.campaign_editor_choices())
        self.assertEqual(actual_output, expected_output)

    @patch('builtins.input', side_effect=['1', 'BAck', '3'])
    def test_create_campaign_valid_back_prompt_case_nominal(self, _):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.display_editor_menu()

        actual_output = mock_stdout.getvalue().strip()
        expected_output = (output.campaign_editor_choices() + '\n' 
                           + output.campaign_editor_choices())
        self.assertEqual(actual_output, expected_output)

    @patch('builtins.input', side_effect=['1', 'bacK', '3'])
    def test_create_campaign_valid_back_prompt_case_min(self, _):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.display_editor_menu()

        actual_output = mock_stdout.getvalue().strip()
        expected_output = (output.campaign_editor_choices() + '\n' 
                           + output.campaign_editor_choices())
        self.assertEqual(actual_output, expected_output)

    @patch('builtins.input', side_effect=['1', 'bac', '9', '2', '3'])
    def test_create_campaign_invalid_back_prompt_min(self, _):
        file_path = os.path.join(self._configs_path, 'bac.bin')
        EditorBBTests.tearDownClass()

        with patch('sys.stdout', new_callable=StringIO):
            self._menu.display_editor_menu()

        self.assertTrue(os.path.isfile(file_path))

    @patch('builtins.input', side_effect=['1', 'try to back out from this', '9', '2', '3'])
    def test_create_campaign_invalid_back_prompt_nominal(self, _):
        file_path = os.path.join(self._configs_path, 'try to back out from this.bin')
        EditorBBTests.tearDownClass()

        with patch('sys.stdout', new_callable=StringIO):
            self._menu.display_editor_menu()

        self.assertTrue(os.path.isfile(file_path))

    # =========================================================== #

    @patch('builtins.input', side_effect=['2', '1', '1', CAMPAIGN_NAME_VALID_MIN, 
                                          '9', '2', '3'])
    def test_rename_campaign_valid_boundary_value_min(self, _):
        EditorBBTests.tearDownClass()
        # Creates file to delete for test
        file_path = os.path.join(self._configs_path, self._file_name)
        self._file_manager.create_config_file(self._campaign)

        file_path = os.path.join(self._configs_path, self.CAMPAIGN_NAME_VALID_MIN + 
                                 EditorBBTests._extension)
        
        with patch('sys.stdout', new_callable=StringIO):
            self._menu.display_editor_menu()
        self.assertTrue(os.path.isfile(file_path))
        
    @patch('builtins.input', side_effect=['2', '1', '1', CAMPAIGN_NAME_VALID_LOWER, 
                                          '9', '2', '3'])
    def test_rename_campaign_valid_boundary_value_lower(self, _):
        EditorBBTests.tearDownClass()
        # Creates file to delete for test
        file_path = os.path.join(self._configs_path, self._file_name)
        self._file_manager.create_config_file(self._campaign)

        file_path = os.path.join(self._configs_path, self.CAMPAIGN_NAME_VALID_LOWER + 
                                 EditorBBTests._extension)
        
        with patch('sys.stdout', new_callable=StringIO):
            self._menu.display_editor_menu()
        self.assertTrue(os.path.isfile(file_path))

    @patch('builtins.input', side_effect=['2', '1', '1', CAMPAIGN_NAME_VALID_NOMINAL, 
                                          '9', '2', '3'])
    def test_rename_campaign_valid_boundary_value_nominal(self, _):
        EditorBBTests.tearDownClass()
        # Creates file to delete for test
        file_path = os.path.join(self._configs_path, self._file_name)
        self._file_manager.create_config_file(self._campaign)

        file_path = os.path.join(self._configs_path, self.CAMPAIGN_NAME_VALID_NOMINAL + 
                                 EditorBBTests._extension)
        
        with patch('sys.stdout', new_callable=StringIO):
            self._menu.display_editor_menu()
        self.assertTrue(os.path.isfile(file_path))

    @patch('builtins.input', side_effect=['2', '1', '1', CAMPAIGN_NAME_VALID_UPPER, 
                                          '9', '2', '3'])
    def test_rename_campaign_valid_boundary_value_upper(self, _):
        EditorBBTests.tearDownClass()
        # Creates file to delete for test
        file_path = os.path.join(self._configs_path, self._file_name)
        self._file_manager.create_config_file(self._campaign)

        file_path = os.path.join(self._configs_path, self.CAMPAIGN_NAME_VALID_UPPER + 
                                 EditorBBTests._extension)
        
        with patch('sys.stdout', new_callable=StringIO):
            self._menu.display_editor_menu()
        self.assertTrue(os.path.isfile(file_path))

    @patch('builtins.input', side_effect=['2', '1', '1', CAMPAIGN_NAME_VALID_MAX, 
                                          '9', '2', '3'])
    def test_rename_campaign_valid_boundary_value_max(self, _):
        EditorBBTests.tearDownClass()
        # Creates file to delete for test
        file_path = os.path.join(self._configs_path, self._file_name)
        self._file_manager.create_config_file(self._campaign)

        file_path = os.path.join(self._configs_path, self.CAMPAIGN_NAME_VALID_MAX + 
                                 EditorBBTests._extension)
        
        with patch('sys.stdout', new_callable=StringIO):
            self._menu.display_editor_menu()
        self.assertTrue(os.path.isfile(file_path))
