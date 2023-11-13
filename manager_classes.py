import os
from json import dump, load, JSONEncoder, decoder
from object_classes import Campaign, Player, NPC, Item, DialogueEvent
import re
from CustomExceptions import forbidden_filename_chars_error as fb
import pickle


BAD_FILENAME_CHARS = r'/\\<>:\"|?*'


class EventsManager:
    def __init__(self):
        self._events_tree = {}

    @property
    def events_tree(self):
        return self._events_tree

    @events_tree.setter
    def events_tree(self, events_tree):
        self._events_tree = events_tree

    def create_event(self, description):
        new_event_id = 0
        while str(new_event_id) in self._events_tree:
            new_event_id += 1
        new_event_id = str(new_event_id)
        created_event = DialogueEvent(new_event_id, description)
        self._events_tree[new_event_id] = created_event

    def edit_event(self, event_id, to_edit, new_value):
        if event_id not in self._events_tree:
            return False
        if to_edit == "description":
            self._events_tree[event_id].description = new_value
        else:
            return False

        return True

    def delete_event(self, event_id):
        is_successful = True
        try:
            del self._events_tree[event_id]
        except KeyError:
            is_successful = False
        return is_successful


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
    
    def edit_campaign_property(self, campaign_prop, prop_name: str, new_prop_value) -> None:       
        if hasattr(campaign_prop, prop_name):
            self._process_new_campaign_name(prop_name, new_prop_value)

            setattr(campaign_prop, prop_name, new_prop_value)
        else:
            print(f"Error: changing invalid campaign property...")

    def _process_new_campaign_name(self, prop_name: str, new_prop_value) -> None:
        if prop_name == 'name' and self._file_manager.is_valid_filename(new_prop_value):
            self._current_campaign.previous_name = self._current_campaign.name
        elif prop_name == 'name' and not self._file_manager.is_valid_filename(new_prop_value):
            raise fb.ForbiddenFilenameCharsError

    def set_current_campaign(self, index: int) -> None:
        self._current_campaign = self._campaigns[index]

    def set_no_current_campaign(self) -> None:
        self._current_campaign = None

    def add_campaign(self, campaign) -> None:
        self._campaigns.append(campaign)

    def campaign_names(self) -> list:
        return [campaign.name for campaign in self._campaigns]

    def save_campaign(self) -> None:
        self._file_manager.save_config_file(self.current_campaign)
        self._current_campaign.previous_name = None

    def create_campaign(self, name: str) -> None:
        if self._file_manager.is_valid_filename(name) is False:
            raise fb.ForbiddenFilenameCharsError
        campaign = Campaign(name)
        self._file_manager.create_config_file(campaign)
        self.add_campaign(campaign)

    def delete_campaign(self) -> None:
        campaign_name = self._current_campaign.name
        self._file_manager.delete_config_file(campaign_name)
        self.campaigns.remove(self.current_campaign)
        self.set_no_current_campaign()

    def load_campaigns(self) -> None:
        self._campaigns = self._file_manager.load_config_files()

    # def rename_campaign(self, new_name) -> None:
    #     if self._file_manager.is_valid_filename(new_name) is False:
    #         raise fb.ForbiddenFilenameCharsError
    #     self._current_campaign.previous_name = self._current_campaign.name
    #     self._current_campaign.name = new_name

    # def edit_description(self, new_desc: str):
    #     self._current_campaign.short_desc = new_desc


# May not need this anymore since we serialize/deserialize campaign object in/from file
class ClassObjEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Player, NPC, Item, DialogueEvent)):
            return obj.__dict__
        return super().default(obj)


class FileManager:
    def __init__(self):
        self._path = 'game_configs/'
        self._config_extension = '.bin'

    def create_config_file(self, campaign: Campaign) -> None:
        try:
            file_name = f'{self._path}{campaign.name}{self._config_extension}'
            with open(file_name, 'xb') as file_object:
                pickle.dump(campaign, file_object)
            file_object.close()
        except FileExistsError:
            raise FileExistsError
        except OSError:
            raise OSError

    def save_config_file(self, campaign: Campaign) -> None:
        try:
            file_name = f'{self._path}{campaign.name}{self._config_extension}'
            if campaign.previous_name:
                os.rename(f'{self._path}{campaign.previous_name}{self._config_extension}',
                           file_name)
            
            with open(file_name, 'wb') as file_object:
                pickle.dump(campaign, file_object)
            file_object.close()
        except OSError:
            raise OSError

    def load_config_files(self) -> list:
        campaign_files = [x for x in os.listdir(self._path) if x.endswith(self._config_extension)]
        parsed_campaigns = list()

        for index, campaign_name in enumerate(campaign_files):
            try:
                with open(f'{self._path}{campaign_name}', 'rb') as file_object:
                    campaign = pickle.load(file_object)
                    parsed_campaigns.append(campaign)
                    file_object.close()
            except decoder.JSONDecodeError:
                print(f"WARNING: config file for campaign {campaign_name} is corrupted. Skipping...")
        return parsed_campaigns

    def delete_config_file(self, file_name) -> None:
        try:
            file_path = f'{self._path}{file_name}{self._config_extension}'
            os.remove(file_path)
        except OSError:
            raise OSError

    def is_valid_filename(self, file_name) -> bool:
        invalid_chars = fr'[{BAD_FILENAME_CHARS}]'
        if re.search(invalid_chars, file_name):
            return False
        return True

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path
