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

    @classmethod
    def setUpClass(cls):
        # Code to set up resources before all tests in this class
        cls._menu = UserMenu()
        cls._file_name = "unittest.bin"
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
        # EditorBBTests.tearDownClass()   
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
