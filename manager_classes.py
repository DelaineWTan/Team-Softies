import abc
import os
from json import dump, load


class Campaign:
    def __init__(self, name, short_desc):
        self._name = name
        self._short_desc = short_desc
        self._sequence_of_events = {}
        self._list_of_PCs = []  # PCs are Characters
        self._list_of_NPCs = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def short_desc(self) -> str:
        return self._short_desc


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
        campaign = Campaign(name, 'some text that should be asked for later in-editor.')
        self._file_manager.create_config_file(campaign)
        self.add_compaign(campaign)

    def delete_campaign(self) -> None:
        self._file_manager.delete_config_file(self._current_campaign.name)
        self.campaigns.remove(self.current_campaign)
        self.set_no_current_campaign()


# should we even do something like this?
class Event(abc.ABC):
    @abc.abstractmethod
    def run_event(self):
        pass


class DialogueEvent(Event):
    def __init__(self, description):
        self._description = description
        self._list_of_choices = []

    def run_event(self):
        print("run the event idk")


class CombatEvent(Event):
    def __init__(self, description):
        self._description = description  # will the combat event have a description?
        self._list_of_choices = []  # idk

    def run_event(self):
        print("run the event idk")


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
