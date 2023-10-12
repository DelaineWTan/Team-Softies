import os
from json import dump, load
from object_classes import Campaign


class CampaignManager:
    def __init__(self) -> None:
        self._campaigns = list()
        self._file_manager = FileManager()
        self._current_campaign = None

    @property
    def campaigns(self) -> list:
        return self._campaigns

    @property
    def current_campaign(self) -> Campaign:
        return self._current_campaign

    def set_current_campaign(self, index: int) -> None:
        # edit to return bool if successful?
        self._current_campaign = self._campaigns[index]

    def set_no_current_campaign(self):
        self._current_campaign = None

    def add_compaign(self, campaign) -> None:
        self._campaigns.append(campaign)

    def campaign_names(self) -> list:
        return [campaign.name for campaign in self._campaigns]

    def create_campaign(self, name: str) -> None:
        campaign = Campaign(name)
        campaign.short_desc = 'some text that should be asked for later in-editor.'
        self._file_manager.create_config_file(campaign)
        self.add_compaign(campaign)

    def delete_campaign(self) -> None:
        self._file_manager.delete_config_file(self._current_campaign.name)
        self.campaigns.remove(self.current_campaign)
        self.set_no_current_campaign()


class FileManager:
    def __init__(self):
        self._path = 'game_configs/'

    def create_config_file(self, campaign: Campaign) -> None:
        with open(f'{self._path}{campaign.name}.json', 'w+') as file_object:
            dump(campaign.__dict__, file_object, indent=3)

    def load_config_files(self):
        pass

    def delete_config_file(self, file_name):
        file_path = f'{self._path}{file_name}.json'
        os.remove(file_path)
