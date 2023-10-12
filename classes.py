import abc
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


    @property
    def campaigns(self) -> list:
        return self._campaigns


    def add_compaign(self, campaign) -> None:
        self._campaigns.append(campaign)


    def campaign_names(self):
        return [campaign.name for campaign in self._campaigns]


    def create_campaign(self, name: str):
        print(name)
        campaign = Campaign(name, 'some text that should be asked for later in-editor.')
        print(campaign)
        self._file_manager.create_config_file(campaign)
        self.add_compaign(campaign)



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
        with open(f'{campaign.name}.json', 'w+') as file_object:
            dump(campaign.__dict__, file_object, indent=3)

    
    def load_config_files(self):
        pass

