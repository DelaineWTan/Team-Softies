from manager_classes import BAD_FILENAME_CHARS


class output_messages:

    @staticmethod
    def campaign_name_prompt():
        return 'Enter new campaign name (Enter back to return to the previous menu):'
    
    @staticmethod
    def invalid_chars_campaign_name(name):
        return f"""{name} is not a valid name for a campaign. {BAD_FILENAME_CHARS}
            cannot be used in a campaign's name."""
    
    @staticmethod
    def invalid_OS_filename(name):
        return f"""{name} is not a valid name for a campaign. Your OS does not
            support this filename for use."""
