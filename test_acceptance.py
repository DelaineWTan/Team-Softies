import unittest
from io import StringIO
from unittest.mock import patch

from main import UserMenu
from output_messages import output_messages as output
from manager_classes import FileManager
from object_classes import Campaign
import os


class MainMenuTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Code to set up resources before all tests in this class
        pass

    @classmethod
    def tearDownClass(cls):
        # Code to clean up resources after all tests in this class
        pass

    def test_select_edit_choice(self):
        # Test scenario 1: Selecting "Edit" choice from the main menu
        # Assertions go here
        pass

    def test_select_play_choice(self):
        # Test scenario 1: Selecting "Play" choice from the main menu
        # Assertions go here
        pass


class EditorMenuTest(unittest.TestCase):
    # Tests only work with an empty game_configs dir

    @classmethod
    def setUpClass(cls):
        # Code to set up resources before all tests in this class
        cls._menu = UserMenu()
        cls._file_name = "unittest.json"
        cls._configs_path = "game_configs"
        cls._file_manager = FileManager()
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
    def test_select_choice_option(self):
        # Test choice event: Selecting a choice option
        # Assertions go here
        pass

    def test_select_end_game_choice(self):
        # Test choice event: Selecting an end game choice option
        # Assertions go here
        pass


if __name__ == '__main__':
    unittest.main()
