import os
from json import dump, load, JSONEncoder, decoder
from object_classes import Campaign, Player, NPC, Item, DialogueEvent
import re
from CustomExceptions import forbidden_filename_chars_error as fb


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

    def create_event(self, description, dialogue):
        new_event_id = 0
        while str(new_event_id) in self._events_tree:
            new_event_id += 1
        new_event_id = str(new_event_id)
        created_event = DialogueEvent(new_event_id, description, dialogue)
        self._events_tree[new_event_id] = created_event

    def edit_event(self, event_id, to_edit, new_value):
        if event_id not in self._events_tree:
            return False
        if to_edit == "description":
            self._events_tree[event_id].description = new_value
        if to_edit == "dialogue":
            self._events_tree[event_id].dialogue = new_value
        else:
            return False

        return True
        # self._events_tree[event_id][to_edit] = new_value

    def delete_event(self, event_id):
        is_successful = True
        try:
            del self._events_tree[event_id]
        except KeyError:
            is_successful = False
        return is_successful

    def link_event(self, event_id_1, event_id_2):
        if event_id_2 in self._events_tree[event_id_1].choices:
            print(f"Event {event_id_1} is already connected to event {event_id_2}")
            print("Returning...")
        else:
            self._events_tree[event_id_1].choices.append(event_id_2)
            print("Link successful!")


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
        # edit to return bool if successful? Would be useful for making
        # custom exceptions
        self._current_campaign = self._campaigns[index]

    def set_no_current_campaign(self) -> None:
        self._current_campaign = None

    def add_campaign(self, campaign) -> None:
        self._campaigns.append(campaign)

    def campaign_names(self) -> list:
        return [campaign.name for campaign in self._campaigns]

    def save_campaign(self):
        self._file_manager.save_config_file(self.current_campaign)

    def create_campaign(self, name: str) -> None:
        if self._file_manager.validate_filename(name) is False:
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

    def rename_campaign(self, new_name) -> None:
        if self._file_manager.validate_filename(new_name) is False:
            raise fb.ForbiddenFilenameCharsError
        self._current_campaign.previous_name = self._current_campaign.name
        self._current_campaign.name = new_name

    def edit_description(self, new_desc: str):
        self._current_campaign.short_desc = new_desc

    def start_campaign(self):
        # get initial event, event 0,
        #
        init_event = self._current_campaign.events["0"]



class ClassObjEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Player, NPC, Item, DialogueEvent)):
            return obj.__dict__
        return super().default(obj)


class FileManager:
    def __init__(self):
        self._path = 'game_configs/'

    def create_config_file(self, campaign: Campaign) -> None:
        try:
            file_name = f'{self._path}{campaign.name}.json'
            with open(file_name, 'x') as file_object:
                dump(campaign.__dict__, file_object, indent=3, cls=ClassObjEncoder)
        except FileExistsError:
            raise FileExistsError
        except OSError:
            raise OSError

    def save_config_file(self, campaign: Campaign) -> None:
        try:
            file_name = f'{self._path}{campaign.previous_name}.json'
            with open(file_name, 'w') as file_object:
                dump(campaign.__dict__, file_object, indent=3, cls=ClassObjEncoder)

            if campaign.name != file_object.name:
                os.rename(file_name, f'{self._path}{campaign.name}.json')
        except FileExistsError:
            raise FileExistsError
        except OSError:
            raise OSError

    def load_config_files(self):
        campaign_files = [x for x in os.listdir(self._path) if x.endswith('.json')]
        parsed_campaigns = list()

        for index, campaign_name in enumerate(campaign_files):
            try:
                with open(f'{self._path}{campaign_name}', 'r') as json_file:
                    json_data = load(json_file)

                    name = json_data['_name']
                    desc = json_data['_short_desc']
                    # events = json_data['_events']
                    # this should work, but haven't tested it yet
                    # @TODO: make it work with CombatEvents as well
                    events = [(key, DialogueEvent(value['_event_id'], value['_description'], value['_choices'])) for
                              key, value in json_data['_events'].items()]
                    events = dict(events)
                    # @TODO properly extract properties of character dicts for players and npcs
                    playable_chars = [Player(player["name"]) for player in json_data['_player_list']]
                    non_playable_chars = [NPC(npc["name"]) for npc in json_data['_npc_list']]
                    items = json_data['_items_list']

                    parsed_campaigns.append(Campaign(name, desc, events, playable_chars,
                                                     non_playable_chars, items))
            except decoder.JSONDecodeError:
                print(f"WARNING: config file for campaign {campaign_name} is corrupted. Skipping...")
        return parsed_campaigns

    def delete_config_file(self, file_name):
        try:
            file_path = f'{self._path}{file_name}.json'
            os.remove(file_path)
        except OSError:
            raise OSError

    def validate_filename(self, file_name) -> bool:
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
