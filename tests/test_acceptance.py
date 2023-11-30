import sys
import os
# Add the path to your project's root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Package Module Imports
import unittest
from unittest.mock import patch
from io import StringIO
import inspect
# Project Module Imports
from main import UserMenu
from output_messages import output_messages as output
from factory_classes import ConfigFileFactory
from object_classes import Campaign


class MainMenuTest(unittest.TestCase):
    def setUp(self):
        # Create a StringIO object to capture printed output
        self.user_menu = UserMenu()

    @patch('builtins.input', side_effect=['1', 'no choice', '3', '3'])  # mock input order (edit, invalid, return, quit)
    def test_select_edit_choice(self, mock_input):
        # Test scenario: Selecting "Edit" choice from the main menu
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.user_menu.display_main_menu()

        printed_output = mock_stdout.getvalue().strip()

        expected_output = ("Welcome to our text-based RPG maker!\n"
                           "1. Editor mode\n2. Player mode\n3. Quit\n"
                           "You are in the editor mode. Choices:\n"
                           "    1. Create new campaign\n    2. Select existing campaign\n    3. Return to main menu\n"
                           "Invalid choice, input should be a number corresponding to the list of choices.\n"
                           "You are in the editor mode. Choices:\n"
                           "    1. Create new campaign\n    2. Select existing campaign\n    3. Return to main menu\n"
                           "Welcome to our text-based RPG maker!\n1. Editor mode\n2. Player mode\n3. Quit")

        self.assertEqual(printed_output, expected_output)

    @patch('builtins.input', side_effect=['2', 'no choice', '2', '3'])  # mock input order (play, invalid, return, quit)
    def test_select_play_choice(self, mock_input):
        # Test scenario: Selecting "Play" choice from the main menu
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.user_menu.display_main_menu()

        printed_output = mock_stdout.getvalue().strip()
        expected_output = inspect.cleandoc("""Welcome to our text-based RPG maker!
                            1. Editor mode
                            2. Player mode
                            3. Quit
                            You are in player mode. Choices:
                            1. Play campaign
                            2. Return to main menu
                            Invalid choice, input should be a number corresponding to the list of choices.
                            You are in player mode. Choices:
                            1. Play campaign
                            2. Return to main menu
                            Welcome to our text-based RPG maker!
                            1. Editor mode
                            2. Player mode
                            3. Quit""")
        self.assertEqual(printed_output, expected_output)


class EditorMenuTest(unittest.TestCase):
    # Tests only work with an empty game_configs dir

    @classmethod
    def setUpClass(cls):
        # Code to set up resources before all tests in this class
        cls._menu = UserMenu()
        cls._file_name = "unittest.bin"
        cls._configs_path = "game_configs"
        cls._file_manager = ConfigFileFactory()
        cls._campaign = Campaign("unittest")

    @classmethod
    def tearDownClass(cls):
        # Code to clean up resources after all tests in this class
        file_path = os.path.join(cls._configs_path, cls._file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

    @patch('builtins.input', side_effect=['1', 'unittest', '9', '2', '3'])
    def test_select_new_campaign(self, mock_input):
        file_path = os.path.join(self._configs_path, self._file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

        new_campaign_text = 'New campaign created: unittest'
        campaign_list = 'Campaign list:\n1. unittest\n2. Back\n'

        # Test scenario 2: Selecting "New campaign" from the editor menu
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.display_editor_menu()
        # Assertions go here
        print_output = mock_stdout.getvalue().strip()
        expected_output = (output.campaign_editor_choices() + '\n' + new_campaign_text + 
                           output.campaign_editing_choices('unittest') + '\n' + campaign_list + 
                           output.campaign_editor_choices())

        self.assertTrue(print_output, expected_output)
        self.assertTrue(os.path.isfile(file_path))

    @patch('builtins.input', side_effect=['2', '2', '3'])
    def test_select_edit_campaign(self, mock_input):
        file_path = os.path.join(self._configs_path, self._file_name)
        if not os.path.isfile(file_path):
            self._file_manager.create_config_file(self._campaign)

        campaign_list = 'Campaign list:\n1. unittest\n2. Back\n'

        # Test scenario 2: Selecting "Edit campaign" from the editor menu
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.display_editor_menu()
        # Assertions go here
        print_output = mock_stdout.getvalue().strip()
        expected_output = (output.campaign_editor_choices() + '\n' + campaign_list + 
                           output.campaign_editor_choices())

        self.assertEqual(print_output, expected_output)

    @patch('builtins.input', side_effect=['2', '1', '7', '1', '3'])
    def test_select_delete_campaign(self, mock_input):
        # Creates file to delete for test
        file_path = os.path.join(self._configs_path, self._file_name)
        if not os.path.isfile(file_path):
            self._file_manager.create_config_file(self._campaign)

        campaign_list = 'Campaign list:\n1. unittest\n2. Back\n'
        post_campaign_list = 'Campaign list:\n'
        post_campaign_list_options = '1. Back\n'

        # Test scenario 2: Selecting "Delete campaign" from the edit campaign menu
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.display_editor_menu()

        # Assertions go here
        print_output = mock_stdout.getvalue().strip()
        expected_output = (output.campaign_editor_choices() + '\n' + campaign_list + 
                           output.campaign_editing_choices(self._campaign.name) + '\n' + 
                           output.delete_campaign(self._campaign.name) + '\n' +  
                           post_campaign_list + output.no_campaigns_available() + '\n' +
                           post_campaign_list_options + output.campaign_editor_choices())

        self.assertEqual(print_output, expected_output)
        self.assertFalse(os.path.isfile(file_path))


class CombatEventTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._menu = UserMenu()

    @classmethod
    def tearDownClass(cls):
        # cls._menu.display_main_menu()
        pass

    @patch('builtins.input', side_effect=['1'])
    def test_select_attack_option(self, mock_input):
        # Test combat event: Selecting "Attack" option
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.run_combat_event()
        # Assertions go here
        printed_output = mock_stdout.getvalue().strip()
        expected_output = ("You are fighting a Level 1 Goblin!\n"
                           "1. Attack\n2. Defend\n3. Use Item\n4. Flee\n"
                           # "Enter your choice (1-4):\n"
                           "You attacked the Level 1 Goblin for 5 damage!\n"
                           "Level 1 Goblin died!")
        self.assertEqual(printed_output, expected_output)
        pass

    @patch('builtins.input', side_effect=['2', '2'])
    def test_select_defend_option(self, mock_input):
        # Test combat event: Selecting "Attack" option
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.run_combat_event()
        # Assertions go here
        printed_output = mock_stdout.getvalue().strip()
        expected_output = ("You are fighting a Level 1 Goblin!\n"
                           "1. Attack\n2. Defend\n3. Use Item\n4. Flee\n"
                           # "Enter your choice (1-4):\n"
                           "You defended yourself!\n"
                           "Level 1 Goblin hit you for 1 damage!")
        self.assertEqual(printed_output, expected_output)
        pass

    @patch('builtins.input', side_effect=['3'])
    def test_select_item_option(self, mock_input):
        # Test combat event: Selecting "Attack" option
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.run_combat_event()
        # Assertions go here
        printed_output = mock_stdout.getvalue().strip()
        expected_output = ("You are fighting a Level 1 Goblin!\n"
                           "1. Attack\n2. Defend\n3. Use Item\n4. Flee\n"
                           # "Enter your choice (1-4):\n"
                           "You used a potion and healed 1 hp!")
        self.assertEqual(printed_output, expected_output)
        pass

    @patch('builtins.input', side_effect=['4'])
    def test_select_flee_option(self, mock_input):
        # Test combat event: Selecting "Attack" option
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.run_combat_event()
        # Assertions go here
        printed_output = mock_stdout.getvalue().strip()
        expected_output = ("You are fighting a Level 1 Goblin!\n"
                           "1. Attack\n2. Defend\n3. Use Item\n4. Flee\n"
                           # "Enter your choice (1-4):\n"
                           "You fled successfully!")
        self.assertEqual(printed_output, expected_output)
        pass


class ChoiceEventTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._menu = UserMenu()

    @classmethod
    def tearDownClass(cls):
        # cls._menu.display_main_menu()
        pass

    @patch('builtins.input', side_effect=['1'])
    def test_select_choice_option(self, mock_input):
        # Test combat event: Selecting "Attack" option
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.run_choice_event()
        # Assertions go here
        printed_output = mock_stdout.getvalue().strip()
        expected_output = ("You encounter a fork in the forest path. What do you do?\n"
                           "1. Take the left path.\n2. Take the right path.\n"
                           "You took the left path.")
        self.assertEqual(printed_output, expected_output)
        pass

    @patch('builtins.input', side_effect=['2'])
    def test_select_end_game_choice(self, mock_input):
        # Test combat event: Selecting "Attack" option
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self._menu.run_choice_event()
        # Assertions go here
        printed_output = mock_stdout.getvalue().strip()
        expected_output = ("You encounter a fork in the forest path. What do you do?\n"
                           "1. Take the left path.\n2. Take the right path.\n"
                           "You took the right path.")
        self.assertEqual(printed_output, expected_output)
        pass


if __name__ == '__main__':
    unittest.main()
