from manager_classes import *
from object_classes import *


# @TODO define campaign entity


class UserMenu:
    def __init__(self):
        self._campaign_manager = CampaignManager()

    def display_main_menu(self):
        # @TODO add load campaign calls to whenever campaigns are shown to the user
        while True:
            print("1. Editor mode")
            print("2. Player mode")
            user_choice = int(input("Enter your choice (1-2):"))
            if user_choice == 1:
                self.display_editor_menu()
                break
            elif user_choice == 2:
                self.display_player_menu()
                break
            else:
                print("Invalid choice, please try again.")

    def display_editor_menu(self):
        while True:
            print("You are in editor mode. Choices:")
            print("1. Create new campaign")
            print("2. Select existing campaign")
            print("3. Return to main menu")
            user_choice = int(input("Enter your choice (1-3):"))
            if user_choice == 1:
                self.display_new_campaign_menu()
                break
            elif user_choice == 2:
                self.display_edit_existing_campaigns_menu()
                break
            elif user_choice == 3:
                self.display_main_menu()
                break
            else:
                print("Invalid choice, please try again.")

    def display_new_campaign_menu(self):
        while True:
            user_input = input("Enter new campaign name:")
            if len(user_input) == 0:
                print("Name cannot be empty, please try again.")
            else:
                self._campaign_manager.create_campaign(user_input)
                self._campaign_manager.set_current_campaign(len(self._campaign_manager.campaigns) - 1)
                print(f"New campaign created: {user_input}")
                self.display_edit_campaign_menu()
                break

    # def display_new_campaign_menu():
    #     while True:
    #         user_input = input("Enter new campaign name:")
    #         if len(user_input) == 0:
    #             print("Name cannot be empty, please try again.")
    #         else:
    #             newCampaign = Campaign(user_input)  # generate new campaign object
    #             campaign_list.append(newCampaign)
    #             print(f"New campaign created: {newCampaign.name}")
    #             display_edit_campaign_menu(newCampaign)
    #             break

    def display_campaign_list_choices(self):
        print("Campaign list:")
        choice_count = 0
        if len(self._campaign_manager.campaigns) == 0:
            print("No campaigns available.")
        else:
            for index, campaign in enumerate(self._campaign_manager.campaign_names()):
                choice_count += 1
                print(f"{index + 1}. {campaign}")
        print(f"{1 + choice_count}. Back")
        return choice_count

    def display_edit_existing_campaigns_menu(self):
        while True:
            self._campaign_manager.load_campaigns()
            choice_count = self.display_campaign_list_choices()
            user_choice = int(input(f"Enter your choice (1-{1 + choice_count}):"))
            if choice_count + 1 > user_choice > 0:
                self._campaign_manager.set_current_campaign(user_choice - 1)
                print(f'--*{self._campaign_manager.current_campaign.name}*--')
                self.display_edit_campaign_menu()
            elif user_choice == 1 + choice_count:
                self.display_editor_menu()
                break
            else:
                print("Invalid choice, please try again.")

    def display_edit_campaign_menu(self):
        # @TODO implement all these campaign management options
        while True:
            print(f"Editing campaign: {self._campaign_manager.current_campaign.name}")
            print("1. Change campaign name")
            print("2. Edit event tree")
            print("3. Manage events")
            print("4. Manage player characters")
            print("5. Manage non-player characters")
            print("6. Manage items")
            print("7. Delete campaign (WARNING: this action is irreversible)")
            print("8. Back")
            user_choice = int(input("Enter your choice (1-8):"))
            if user_choice == 1:
                self.edit_campaign_name_menu()
            elif user_choice == 4:
                self.manage_campaign_players()
            elif 1 <= user_choice <= 6:
                print("Made a valid choice 1-6")
            elif user_choice == 7:
                self._campaign_manager.delete_campaign()
                break
            elif user_choice == 8:
                self._campaign_manager.set_no_current_campaign()
                self.display_edit_existing_campaigns_menu()
                break
            else:
                print("Invalid choice, please try again.")

    def edit_campaign_name_menu(self):
        while True:
            user_input = input("Enter new campaign name:")
            if len(user_input) == 0:
                print("Name cannot be empty, please try again.")
            else:
                self._campaign_manager.rename_campaign(user_input)
                self._campaign_manager.save_campaign()
                break

    # generic function to change any property in campaign
    def _change_campaign_property(self, campaign_obj, prop_name: str, current_prop: str, display_prop):
        print(f"Current {display_prop}: {current_prop}")
        new_property = input(f"Enter new {display_prop}: ")
        if hasattr(campaign_obj, prop_name):
            setattr(campaign_obj, prop_name, new_property)
        else:
            print(f"Error: changing invalid campaign property...")

    def display_player_menu(self):
        while True:
            print("You are in player mode. Choices:")
            print("1. Play campaign")
            print("2. Return to main menu")
            user_choice = int(input("Enter your choice (1-2):"))
            if user_choice == 1:
                self.display_play_existing_campaigns_menu()
                break
            elif user_choice == 2:
                self.display_main_menu()
                break
            else:
                print("Invalid choice, please try again.")

    def manage_campaign_players(self):
        while True:
            print(f" --Player Character List-- ")
            for index, player in enumerate(self._campaign_manager.current_campaign.player_list):
                print(f"{index + 1}. {player.name}")
            player_index = int(
                input(f"Enter your choice (1-{len(self._campaign_manager.current_campaign.player_list)}):")) - 1
            if 0 <= player_index <= (len(self._campaign_manager.current_campaign.player_list)):
                self.manage_single_campaign_player(player_index)
                break
            else:
                print("Invalid choice, please try again.")

    def manage_single_campaign_player(self, player_index):
        while True:
            print(f" --Player Character Details-- ")
            print(f"{self._campaign_manager.current_campaign.player_list[player_index]}")
            print(f" -------- ")
            print("1. Change player name")
            print("2. Change player description")
            print("3. Change player base hit points")
            print("4. Change player base attack")
            print("5. Change player base speed")
            print("6. Change player level up experience")
            print("7. Change player max level")
            print("8. Change player hit point gain per level")
            print("9. Change player attack gain per level")
            print("10. Change player speed gain per level")
            print("11. Clear character")
            print("12. Back")

            user_choice = int(input("Enter your choice (1-12):"))
            if user_choice == 1:
                self._change_campaign_property(self._campaign_manager.current_campaign.player_list[player_index]
                                               , "name",
                                               self._campaign_manager.current_campaign.player_list[player_index].name
                                               , "name")
                # self._campaign_manager.current_campaign.player_list[player_index].name = new_name
                continue
            if user_choice == 2:
                self._change_campaign_property(self._campaign_manager.current_campaign.player_list[player_index]
                                          , "description",
                                          self._campaign_manager.current_campaign.player_list[player_index].description
                                          , "description")
                continue
            if user_choice == 3:
                self._change_campaign_property(self._campaign_manager.current_campaign.player_list[player_index], "base_hp",
                                          self._campaign_manager.current_campaign.player_list[player_index].base_hp
                                          , "base hit points")
                continue
            if user_choice == 4:
                self._change_campaign_property(self._campaign_manager.current_campaign.player_list[player_index], "base_atk",
                                          self._campaign_manager.current_campaign.player_list[player_index].base_atk
                                          , "base attack")
                continue
            if user_choice == 5:
                self._change_campaign_property(self._campaign_manager.current_campaign.player_list[player_index], "base_spd",
                                          self._campaign_manager.current_campaign.player_list[player_index].base_spd
                                          , "base speed")
                continue
            if user_choice == 6:
                self._change_campaign_property(self._campaign_manager.current_campaign.player_list[player_index]
                                          , "exp_per_lvl_up",
                                          self._campaign_manager.current_campaign.player_list[player_index].exp_per_lvl_up
                                          , "level up experience")
                continue
            if user_choice == 7:
                self._change_campaign_property(self._campaign_manager.current_campaign.player_list[player_index], "max_lvl",
                                          self._campaign_manager.current_campaign.player_list[player_index].max_lvl
                                          , "max level")
                continue
            if user_choice == 8:
                self._change_campaign_property(self._campaign_manager.current_campaign.player_list[player_index], "hp_mod",
                                          self._campaign_manager.current_campaign.player_list[player_index].hp_mod
                                          , "hit point gain per level")
                continue
            if user_choice == 9:
                self._change_campaign_property(self._campaign_manager.current_campaign.player_list[player_index], "atk_mod",
                                          self._campaign_manager.current_campaign.player_list[player_index].atk_mod
                                          , "attack gain per level")
                continue
            if user_choice == 10:
                self._change_campaign_property(self._campaign_manager.current_campaign.player_list[player_index], "spd_mod",
                                          self._campaign_manager.current_campaign.player_list[player_index].spd_mod
                                          , "speed gain per level")
                continue
            if user_choice == 12:
                break
            else:
                print("Invalid choice, please try again.")

    def display_play_existing_campaigns_menu(self):
        while True:
            choice_count = self.display_campaign_list_choices()
            user_choice = int(input(f"Enter your choice (1-{1 + choice_count}):"))
            if choice_count + 1 > user_choice > 0:
                self.start_campaign(campaign_list[user_choice - 1])
            elif user_choice == 1 + choice_count:
                self.display_player_menu()
                break
            else:
                print("Invalid choice, please try again.")

    def start_campaign(self):
        # @TODO properly extract campaign data to start campaign event sequence
        self.run_combat_event()
        self.run_choice_event()
        # game ended, return to main menu
        self.run_last_choice_event()
        print("Campaign ended!")
        print("########################################################################")
        self.display_main_menu()

    # @TODO Fake combat event
    def run_combat_event(self):
        enemy_name = "Level 1 Goblin"
        while True:
            print(f"You are fighting a {enemy_name}!")
            print("1. Attack")
            print("2. Defend")
            print("3. Use Item")
            print("4. Flee")
            user_choice = int(input(f"Enter your choice (1-4):"))
            if user_choice == 1:
                print(f"You attacked the {enemy_name} for 5 damage!")
                print(f"{enemy_name} died!")
                break
            elif user_choice == 2:
                print("You defended yourself!")
                print(f"{enemy_name} hit you for 1 damage!")
            elif user_choice == 3:
                self.use_item_menu()
            elif user_choice == 4:
                print("You fled successfully!")
                break
            else:
                print("Invalid choice, please try again.")

    # @TODO fake use item menu
    def use_item_menu(self):
        print("You used a potion and healed 1 hp!")

    # @TODO Fake choice event
    def run_choice_event(self):
        while True:
            print("You encounter a fork in the forest path. What do you do?")
            print("1. Take the left path.")
            print("2. Take the right path.")
            user_choice = int(input("Enter your choice (1-2):"))
            if user_choice == 1:
                print("You took the left path.")
                break
            elif user_choice == 2:
                print("You took the right path.")
                break
            else:
                print("Invalid choice, please try again.")

    # @TODO Fake ending choice run_choice_event
    def run_last_choice_event(self):
        while True:
            print("You reach the end of the path and discover 2 treasure chests. Which one do you pick?")
            print("1. Pick the red treasure chest.")
            print("2. Pick the blue treasure chest.")
            user_choice = int(input("Enter your choice (1-2):"))
            if user_choice == 1:
                print("You picked the red treasure chest.")
                print("The red treasure chest was booby trapped, you died in the explosion.")
                print("Defeat!")
                break
            elif user_choice == 2:
                print("You picked the blue treasure chest.")
                print("The blue treasure chest contains the holy grail. You found it!")
                print("Victory!")
                break
            else:
                print("Invalid choice, please try again.")


if __name__ == '__main__':
    print(f'Welcome to our text-based RPG maker!')
    menu = UserMenu()
    menu.display_main_menu()
