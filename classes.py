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


    @property
    def campaigns(self) -> list:
        return self._campaigns


    def add_compaign(campaign) -> None:
        self._campaigns.add(campaign)


    def campaign_names():
        return [campaign.name for campaign in self._campaigns]



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
    def __init__():
        self._path


    def create_config_file(campaign: Campaign) -> None:
        with open(f'{campaign.name}.json', 'w+') as file_object:
            dump(campaign.__dict__, file_object, indent=3)

    
    def load_config_files():
        pass

