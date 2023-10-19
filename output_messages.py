from manager_classes import BAD_FILENAME_CHARS


class output_messages:

    @staticmethod
    def campaign_name_prompt():
        return 'Enter new campaign name (Enter back to return to the previous menu):'
    
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
