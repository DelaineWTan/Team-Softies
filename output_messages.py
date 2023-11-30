from factory_classes import BAD_FILENAME_CHARS



class output_messages:

    @staticmethod
    def campaign_editing_choices(campaign_name: str) -> str:
        return f"""Editing campaign: {campaign_name}
    1. Rename campaign
    2. Edit event tree
    3. Manage events
    4. Manage player characters
    5. Manage non-player characters
    6. Manage items
    7. Delete campaign (WARNING: this action is irreversible)
    8. Edit campaign description
    9. Back"""

    
    @staticmethod
    def campaign_editor_choices() -> str:
        return """You are in the editor mode. Choices:
    1. Create new campaign
    2. Select existing campaign
    3. Return to main menu"""


    @staticmethod
    def campaign_name_prompt():
        return 'Enter new campaign name (Enter back to return to the previous menu):'


    @staticmethod
    def no_campaigns_available():
        return 'No campaigns available.'


    @staticmethod
    def delete_campaign(campaign_name: str):
        return f'Deleted campaign: {campaign_name}'


    @staticmethod
    def invalid_choice():
        return 'Invalid choice, please try again.'
    
    
    @staticmethod
    def invalid_choice_int_expected():
        return 'Invalid choice, input should be a number corresponding to the list of choices.'
    
    
    @staticmethod
    def invalid_chars_campaign_name(name: str) -> str:
        return f"""{name} is not a valid name for a campaign. {BAD_FILENAME_CHARS}
            cannot be used in a campaign's name."""
    
    
    @staticmethod
    def invalid_OS_filename(name: str) -> str:
        return f"""{name} is not a valid name for a campaign. Your OS does not
            support this filename for use."""
    
    
    @staticmethod
    def delete_missing_config_file(filename: str) -> str:
        return f'\'{filename}\' cannot be deleted since it is not in the game_configs folder.'
