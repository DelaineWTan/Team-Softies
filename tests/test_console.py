import unittest
from unittest.mock import patch
from io import StringIO
from main import UserMenu


class TestStringMethods(unittest.TestCase):
    @patch('builtins.input',
           side_effect=['1', '3', '3'])  # mock input order (edit, return to menu, quit)
    def test_menu_editor_back_quit(self, _):
        with patch('sys.stdout',
                   new_callable=StringIO) as mock_stdout:  # extract all print on screen into a
            # string
            menu = UserMenu()
            menu.display_main_menu()

        printed_output = mock_stdout.getvalue()  # Get the printed output

        self.assertEqual(printed_output,
                         "Welcome to our text-based RPG maker!\n1. Editor mode\n"
                         "2. Player mode\n3. "
                         "Quit\nYou are in the editor mode. Choices:\n    1. Create new "
                         "campaign\n    "
                         "2. Select existing campaign\n    3. Return to main menu\n"
                         "Welcome to our text-based RPG maker!\n1. Editor mode\n2. Player mode\n"
                         "3. Quit\n")

    @patch('builtins.input', side_effect=['1', 'no choice', '3',
                                          '3'])  # mock input order (edit, invalid, return, quit)
    def test_menu_editor_invalid_option(self, _):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            menu = UserMenu()
            menu.display_main_menu()

        printed_output = mock_stdout.getvalue().strip()

        self.assertEqual(printed_output,
                         "Welcome to our text-based RPG maker!\n1. Editor mode\n2. Player "
                         "mode\n3. "
                         "Quit\nYou are in the editor mode. Choices:\n    1. Create new "
                         "campaign\n    "
                         "2. Select existing campaign\n    3. Return to main menu\nInvalid choice, "
                         "input should be a number corresponding to the list of choices.\nYou are "
                         "in "
                         "the editor mode. Choices:\n    1. Create new campaign\n    2. Select "
                         "existing campaign\n    3. Return to main menu\n"
                         "Welcome to our text-based RPG maker!\n"
                         "1. Editor mode\n2. Player mode\n3. Quit")

    @patch('builtins.input', return_value='3')
    def test_quit_game_immediately(self, _):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            menu = UserMenu()
            menu.display_main_menu()

        printed_output = mock_stdout.getvalue().strip()
        after_output = printed_output.strip()

        self.assertEqual(after_output,
                         "Welcome to our text-based RPG maker!\n1. Editor mode\n2. Player "
                         "mode\n3. Quit")


if __name__ == '__main__':
    unittest.main()
