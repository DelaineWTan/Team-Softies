import os
import re
import pickle
from json import decoder
from object_classes import Campaign, DialogueEvent
from CustomExceptions import forbidden_filename_chars_error as fb

BAD_FILENAME_CHARS = r'/\\<>:\"|?*'


class EventFactory:
    events_tree = {}

    @staticmethod
    def create_event(description, dialogue):
        new_event_id = 0
        while str(new_event_id) in EventFactory.events_tree:
            new_event_id += 1
        new_event_id = str(new_event_id)
        created_event = DialogueEvent(new_event_id, description, dialogue)
        EventFactory.events_tree[new_event_id] = created_event

    @staticmethod
    def edit_event(event_id, to_edit, new_value):
        if event_id not in EventFactory.events_tree:
            return False
        if to_edit == "description":
            EventFactory.events_tree[event_id].description = new_value
        if to_edit == "dialogue":
            EventFactory.events_tree[event_id].dialogue = new_value
        else:
            return False

        return True

    @staticmethod
    def delete_event(event_id):
        is_successful = True
        try:
            del EventFactory.events_tree[event_id]
        except KeyError:
            is_successful = False
        return is_successful

    @staticmethod
    def link_event(event_id_1, event_id_2):
        EventFactory.events_tree[event_id_1].choices.append(event_id_2)


class CampaignFactory:
    campaigns = []
    current_campaign = None

    @staticmethod
    def set_current_campaign(index: int) -> None:
        CampaignFactory.current_campaign = CampaignFactory.campaigns[index]

    @staticmethod
    def set_no_current_campaign() -> None:
        CampaignFactory.current_campaign = None

    @staticmethod
    def add_campaign(campaign) -> None:
        CampaignFactory.campaigns.append(campaign)

    @staticmethod
    def campaign_names() -> list:
        return [campaign.name for campaign in CampaignFactory.campaigns]

    @staticmethod
    def save_campaign() -> None:
        ConfigFileFactory.save_config_file(CampaignFactory.current_campaign)
        CampaignFactory.current_campaign.previous_name = None

    @staticmethod
    def create_campaign(name: str) -> None:
        if ConfigFileFactory.validate_filename(name) is False:
            raise fb.ForbiddenFilenameCharsError
        campaign = Campaign(name)
        ConfigFileFactory.create_config_file(campaign)
        CampaignFactory.add_campaign(campaign)

    @staticmethod
    def delete_campaign() -> None:
        campaign_name = CampaignFactory.current_campaign.name
        ConfigFileFactory.delete_config_file(campaign_name)
        CampaignFactory.campaigns.remove(CampaignFactory.current_campaign)
        CampaignFactory.set_no_current_campaign()

    @staticmethod
    def load_campaigns() -> None:
        CampaignFactory.campaigns = ConfigFileFactory.load_config_files()

    @staticmethod
    def edit_campaign_property(campaign_prop, prop_name: str, new_prop_value) -> None:       
        if hasattr(campaign_prop, prop_name):
            CampaignFactory._process_new_campaign_name(prop_name, new_prop_value)

            setattr(campaign_prop, prop_name, new_prop_value)
        else:
            print(f"Error: changing invalid campaign property...")

    @staticmethod
    def _process_new_campaign_name(prop_name: str, new_prop_value) -> None:
        if prop_name == 'name' and ConfigFileFactory.validate_filename(new_prop_value):
            CampaignFactory.current_campaign.previous_name = CampaignFactory.current_campaign.name
        elif prop_name == 'name' and not ConfigFileFactory.validate_filename(new_prop_value):
            raise fb.ForbiddenFilenameCharsError

    @staticmethod
    def rename_campaign(new_name) -> None:
        if ConfigFileFactory.validate_filename(new_name) is False:
            raise fb.ForbiddenFilenameCharsError
        CampaignFactory.current_campaign.previous_name = CampaignFactory.current_campaign.name
        CampaignFactory.current_campaign.name = new_name

    @staticmethod
    def edit_description(new_desc: str):
        CampaignFactory.current_campaign.short_desc = new_desc


class ConfigFileFactory:
    _path = 'game_configs/'
    _config_extension = '.bin'

    @staticmethod
    def create_config_file(campaign: Campaign) -> None:
        try:
            file_name = f'{ConfigFileFactory._path}{campaign.name}{ConfigFileFactory._config_extension}'
            with open(file_name, 'xb') as file_object:
                pickle.dump(campaign, file_object)
            file_object.close()
        except FileExistsError:
            raise FileExistsError
        except OSError:
            raise OSError

    @staticmethod
    def save_config_file(campaign: Campaign) -> None:
        try:
            file_name = f'{ConfigFileFactory._path}{campaign.name}{ConfigFileFactory._config_extension}'
            if campaign.previous_name:
                os.rename(f'{ConfigFileFactory._path}{campaign.previous_name}{ConfigFileFactory._config_extension}', file_name)

            with open(file_name, 'wb') as file_object:
                pickle.dump(campaign, file_object)
            file_object.close()
        except OSError:
            raise OSError

    @staticmethod
    def load_config_files() -> list:
        campaign_files = [x for x in os.listdir(ConfigFileFactory._path) if x.endswith(ConfigFileFactory._config_extension)]
        parsed_campaigns = list()

        for index, campaign_name in enumerate(campaign_files):
            try:
                with open(f'{ConfigFileFactory._path}{campaign_name}', 'rb') as file_object:
                    campaign = pickle.load(file_object)
                    parsed_campaigns.append(campaign)
                    file_object.close()
            except decoder.JSONDecodeError:
                print(f"WARNING: config file for campaign {campaign_name} is corrupted. Skipping...")
        return parsed_campaigns

    @staticmethod
    def delete_config_file(file_name) -> None:
        try:
            file_path = f'{ConfigFileFactory._path}{file_name}{ConfigFileFactory._config_extension}'
            os.remove(file_path)
        except OSError:
            raise OSError

    @staticmethod
    def validate_filename(file_name) -> bool:
        invalid_chars = fr'[{BAD_FILENAME_CHARS}]'
        if re.search(invalid_chars, file_name):
            return False

        return True

    @property
    def path(self):
        return ConfigFileFactory._path

    @path.setter
    def path(self, path):
        ConfigFileFactory._path = path
