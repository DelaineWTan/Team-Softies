import os
import re
import pickle
import shutil
from json import decoder
from object_classes import Campaign, DialogueEvent, Player, NPC, Character
from CustomExceptions import forbidden_filename_chars_error as fb

BAD_FILENAME_CHARS = r'/\\<>:\"|?*'


class EventFactory:
    events_tree = {}

    @staticmethod
    def combat_attack(attacker: Character, defender: Character):
        # critical hit mod
        # hit_mod = random.random()
        #
        # if hit_mod <= 0.1:
        #    print("A critical Hit!")
        #    hit_mod = 1.2
        # else:
        hit_mod = 1
        damage = attacker.base_atk * hit_mod
        print(f"{attacker.name} attacked {defender.name} for {damage} damage!")
        defender.current_hp -= damage

    @staticmethod
    def use_item_menu(player: Player):
        print("You used a potion and healed 3 hp!")
        player.current_hp += 3
        if player.current_hp > player.max_hp:
            player.current_hp = player.max_hp

    @staticmethod
    def run_combat_event(player: Player, enemy: NPC) -> Player:
        print(f"You engaged combat with {enemy.name}!")
        while True:
            print(f"You are fighting {enemy.name}!")
            print(f"{player.name} HP: {player.current_hp}/{player.max_hp}")
            print(f"{enemy.name} HP: {enemy.current_hp}/{enemy.max_hp}")
            print("1. Attack")
            print("2. Defend")
            print("3. Use Item")
            print("4. Flee")
            user_choice = int(input(f"Enter your choice (1-4):"))
            if user_choice == 1:
                # @TODO max hp and current hp are still using default values
                if player.base_spd >= enemy.base_spd:
                    print(f"You attack first!")
                    EventFactory.combat_attack(player, enemy)
                    if enemy.current_hp <= 0:
                        print(f"You defeated {enemy.name}!")
                        print(f"You gained {enemy.exp} experience.")
                        break
                    print(f"{enemy.name} attacks!")
                    EventFactory.combat_attack(enemy, player)
                    if player.current_hp <= 0:
                        print(f"You were defeated...")
                        break
                else:
                    print(f"{enemy.name} attacks!")
                    EventFactory.combat_attack(enemy, player)
                    if player.current_hp <= 0:
                        print(f"You were defeated...")
                        break
                    print(f"You attack!")
                    EventFactory.combat_attack(player, enemy)
                    if enemy.current_hp <= 0:
                        print(f"You defeated {enemy.name}!")
                        print(f"You gained {enemy.exp} experience.")
                        break
            elif user_choice == 2:
                print("You defended yourself!")
                print(f"{enemy.name} hit you for 1 damage!")
                player.current_hp -= 1
            elif user_choice == 3:
                EventFactory.use_item_menu(player)
            elif user_choice == 4:
                print("You fled successfully!")
                break
            else:
                print("Invalid choice, please try again.")

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
        EventFactory.events_tree.pop(event_id)
        for event in EventFactory.events_tree.values():
            if event_id in event.choices:
                event.choices.remove(event_id)

    @staticmethod
    def link_event(event_id_1, event_id_2):
        EventFactory.events_tree[event_id_1].choices.append(event_id_2)

    @staticmethod
    def print_events():
        # for event in EventFactory.events_tree.values():
        #     print(f"| {event.event_id} : {event.description} -> {event.choices}")
        list(map(lambda event: print(f"| {event.event_id} : {event.description} -> {event.choices}"),
                 EventFactory.events_tree.values()))

    @staticmethod
    def start_events(player: Player, npc: NPC):
        # get initial event, event 0
        init_event = EventFactory.events_tree["0"]
        temp_event = init_event
        # print event 0
        while len(temp_event.choices) != 0:
            print(f"| -=+ {temp_event.description} +=-")
            print(f"| {temp_event.dialogue}")

            # @TODO handle combat event somehow else
            if "combat" in temp_event.description.lower().strip():
                EventFactory.run_combat_event(player, npc)

            print("Choose an option:")
            choice_count = 1
            count_to_choices = {}
            for n in temp_event.choices:
                print(f"{choice_count}. Choice {n}")
                count_to_choices[choice_count] = n
                choice_count += 1
            player_choice = int(input("Choice: "))
            temp_event = EventFactory.events_tree[count_to_choices[player_choice]]
        print(f"| -=+ {temp_event.description} +=-")
        print(f"| {temp_event.dialogue}")
        print("Campaign ended. Going back to campaign list...")


class CampaignFactory:
    CAMPAIGN_NAME_LEN_MIN = 1
    CAMPAIGN_NAME_LEN_MAX = 125

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
        ConfigFileFactory.save_config_backup_file(CampaignFactory.current_campaign)
        CampaignFactory.current_campaign.previous_name = None

    @staticmethod
    def create_campaign(name: str) -> None:
        if ConfigFileFactory.validate_filename(name) is False:
            raise fb.ForbiddenFilenameCharsError
        campaign = Campaign(name)
        ConfigFileFactory.create_config_file(campaign)
        ConfigFileFactory.save_config_backup_file(campaign)
        CampaignFactory.add_campaign(campaign)


    @staticmethod
    def delete_campaign() -> None:
        campaign_name = CampaignFactory.current_campaign.name
        ConfigFileFactory.delete_config_file(campaign_name)
        ConfigFileFactory.delete_config_backup_file(campaign_name)
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
            print("Error: changing invalid campaign property...")

    @staticmethod
    def _process_new_campaign_name(prop_name: str, new_prop_value) -> None:
        if prop_name == 'name' and ConfigFileFactory.validate_filename(new_prop_value):
            CampaignFactory.current_campaign.previous_name = CampaignFactory.current_campaign.name
        elif prop_name == 'name' and not ConfigFileFactory.validate_filename(new_prop_value):
            raise fb.ForbiddenFilenameCharsError


class ConfigFileFactory:
    _path = 'game_configs/'
    _config_extension = '.bin'
    _config_backup_extension = '.bin.bak'

    @staticmethod
    def create_config_file(campaign: Campaign) -> None:
        try:
            file_name = (f'{ConfigFileFactory._path}{campaign.name}'
                         f'{ConfigFileFactory._config_extension}')
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
            file_name = (f'{ConfigFileFactory._path}{campaign.name}'
                         f'{ConfigFileFactory._config_extension}')
            if campaign.previous_name:
                os.rename(
                    f'{ConfigFileFactory._path}{campaign.previous_name}'
                    f'{ConfigFileFactory._config_extension}',
                    file_name)

            with open(file_name, 'wb') as file_object:
                pickle.dump(campaign, file_object)
                file_object.flush()
            file_object.close()
        except OSError:
            raise OSError

    @staticmethod
    def save_config_backup_file(campaign: Campaign) -> None:
        try:
            file_name = (f'{ConfigFileFactory._path}{campaign.name}'
                         f'{ConfigFileFactory._config_extension}')
            bak_path = (f'{ConfigFileFactory._path}{campaign.name}'
                        f'{ConfigFileFactory._config_backup_extension}')
            if campaign.previous_name:
                print(bak_path)
                print(f'{ConfigFileFactory._path}{campaign.previous_name}'
                      f'{ConfigFileFactory._config_backup_extension}')
                os.rename(
                    f'{ConfigFileFactory._path}{campaign.previous_name}'
                    f'{ConfigFileFactory._config_backup_extension}',
                    bak_path)
            shutil.copy(file_name, bak_path)
        except OSError:
            raise OSError

    @staticmethod
    def load_config_files() -> list:
        campaign_files = [x for x in os.listdir(ConfigFileFactory._path) if
                          x.endswith(ConfigFileFactory._config_extension)]
        parsed_campaigns = list()

        for index, campaign_name in enumerate(campaign_files):
            try:
                with open(f'{ConfigFileFactory._path}{campaign_name}', 'rb') as file_object:
                    campaign = pickle.load(file_object)
                    parsed_campaigns.append(campaign)
                    file_object.close()
            except (decoder.JSONDecodeError, pickle.UnpicklingError):
                print(
                    f"WARNING: config file for campaign {campaign_name} is corrupted. Checking for backup...")
                if ConfigFileFactory.restore_backup_file(campaign_name):
                    try:
                        with open(f'{ConfigFileFactory._path}{campaign_name}', 'rb') as file_object:
                            campaign = pickle.load(file_object)
                            parsed_campaigns.append(campaign)
                            file_object.close()
                    except (decoder.JSONDecodeError, pickle.UnpicklingError):
                        print(
                            f"WARNING: config file for campaign {campaign_name} is corrupted. Skipping...")
                else:
                    print(
                        f"WARNING: config file for campaign {campaign_name} is could not be restored. Skipping...")
        return parsed_campaigns

    @staticmethod
    def restore_backup_file(campaign_name_ext) -> bool:
        campaign_name = campaign_name_ext.split('.')[0]
        file_name = (f'{ConfigFileFactory._path}{campaign_name}'
                     f'{ConfigFileFactory._config_extension}')
        print(campaign_name)
        bak_path = (f'{ConfigFileFactory._path}{campaign_name}'
                    f'{ConfigFileFactory._config_backup_extension}')
        try:
            shutil.copy(bak_path, file_name)
            return True
        except (IsADirectoryError, PermissionError, shutil.SpecialFileError):
            return False
        except (IOError, OSError):
            print(
                f"WARNING: backup file for campaign {campaign_name} does not exist...")
            return False

    @staticmethod
    def delete_config_file(file_name) -> None:
        try:
            file_path = f'{ConfigFileFactory._path}{file_name}{ConfigFileFactory._config_extension}'
            os.remove(file_path)
        except OSError:
            raise OSError

    @staticmethod
    def delete_config_backup_file(file_name) -> None:
        try:
            file_path = f'{ConfigFileFactory._path}{file_name}{ConfigFileFactory._config_backup_extension}'
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
