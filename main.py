from factory_classes import *
from object_classes import *
from output_messages import output_messages as output


BACK_KEYWORD = 'back'


class UserMenu:
    def __init__(self):
        self._campaign_factory = CampaignFactory
        self._events_factory = EventFactory

    def display_main_menu(self):
        while True:
            print(f'Welcome to our text-based RPG maker!')
            print("1. Editor mode")
            print("2. Player mode")
            print("3. Quit")
            user_choice = int(input("Enter your choice (1-2):"))
            if user_choice == 1:
                self.display_editor_menu()
                continue
            elif user_choice == 2:
                self.display_player_menu()
                break
            elif user_choice == 3:
                return
            else:
                print(output.invalid_choice())

    def display_editor_menu(self):
        while True:
            print(output.campaign_editor_choices())
            try:
                user_choice = int(input("Enter your choice (1-3):"))
                if user_choice == 1:
                    self.display_new_campaign_menu()
                elif user_choice == 2:
                    self.display_edit_existing_campaigns_menu()
                    continue
                elif user_choice == 3:
                    # Wouldn't this run another instance of display_main_menu
                    # and never finishing the display_main_menu from before?
                    # Unless I'm getting it wrong
                    # -Jun
                    # self.display_main_menu()
                    break
                else:
                    print("Invalid choice, please try again.")
            except ValueError:
                print(output.invalid_choice_int_expected())

    def display_new_campaign_menu(self):
        while True:
            user_input = None
            try:
                user_input = input(output.campaign_name_prompt()).strip()
                if len(user_input) == 0:
                    raise ValueError
                elif user_input.lower() == BACK_KEYWORD:
                    break

                self._campaign_factory.create_campaign(user_input)
                self._campaign_factory.set_current_campaign(len(self._campaign_factory.campaigns) - 1)
                print(f"New campaign created: {user_input}")
                self.display_edit_campaign_menu(True)
                break
            except FileExistsError:
                print(f'{user_input} already exists as another name.')
            except ValueError:
                print("Name cannot be empty, please try again.")
            except OSError:
                print(output.invalid_OS_filename(user_input))
            except fb.ForbiddenFilenameCharsError:
                print(output.invalid_chars_campaign_name(user_input))

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
        if len(self._campaign_factory.campaigns) == 0:
            print(output.no_campaigns_available())
        else:
            for index, campaign in enumerate(self._campaign_factory.campaign_names()):
                choice_count += 1
                print(f"{index + 1}. {campaign}")
        print(f"{1 + choice_count}. Back")
        return choice_count

    def display_edit_existing_campaigns_menu(self):
        while True:
            try:
                self._campaign_factory.load_campaigns()
                choice_count = self.display_campaign_list_choices()
                user_choice = int(input(f"Enter your choice (1-{1 + choice_count}):"))
                if choice_count + 1 > user_choice > 0:
                    self._campaign_factory.set_current_campaign(user_choice - 1)
                    # print(f'--*{self._campaign_manager.current_campaign.name}*--')
                    self.display_edit_campaign_menu(False)
                    continue
                elif user_choice == 1 + choice_count:
                    # self.display_editor_menu()
                    break
                else:
                    print("Invalid choice, please try again.")
            except ValueError:
                print(output.invalid_choice_int_expected())

    def display_edit_campaign_menu(self, from_campaign_creation):
        # @TODO implement all these campaign management options
        while True:
            print(output.campaign_editing_choices(self._campaign_factory.current_campaign.name))
            try:
                user_choice = int(input("Enter your choice (1-8):"))
                if user_choice == 1:
                    self._change_campaign_property_menu(self._campaign_manager.current_campaign, 'name', 'Campaign Name')
                elif user_choice == 2:
                    self.edit_events_menu()
                elif user_choice == 4:
                    self.manage_campaign_players()
                elif 1 <= user_choice <= 6:
                    print("Made a valid choice 1-6")
                elif user_choice == 7:
                    self.delete_campaign(self._campaign_factory.current_campaign.name)
                    if from_campaign_creation:
                        self.display_edit_existing_campaigns_menu()
                    break
                elif user_choice == 8:
                    self._change_campaign_property_menu(self._campaign_manager.current_campaign, 'short_desc', 'Campaign Description')
                elif user_choice == 9:
                    self._campaign_factory.set_no_current_campaign()
                    if from_campaign_creation:
                        self.display_edit_existing_campaigns_menu()
                    break
                else:
                    print(output.invalid_choice())
            except ValueError:
                print(output.invalid_choice_int_expected())
            except AttributeError:
                print("caught attr error")

    def delete_campaign(self, campaign_name: str) -> None:
        try:
            print(output.delete_campaign(campaign_name))
            self._campaign_factory.delete_campaign()
        except OSError:
            print(output.delete_missing_config_file(campaign_name))

    # Edit events stuff start -Jun ==========================
    def edit_events_menu(self):
        # @TODO: potentially have a case where when it breaks, it still saves the
        #   events so that the files don't get corrupted. Same should go for campaigns,
        #   if it's not implemented yet.
        self._events_factory.events_tree = self._campaign_factory.current_campaign.events
        user_choice = None
        while user_choice != 4:
            # @TODO: print tree structure here
            print("printing event tree here...")
            # print(self._events_manager.events_tree)
            for event in self._events_factory.events_tree.values():
                print(f"|| Event ID: {event.event_id} -> choices: {event.choices}")
            print("1. Create new event\n"
                  "2. Edit an existing event\n"
                  "3. Link events (create choices)\n"
                  "4. Return to edit campaign menu")
            user_choice = int(input("Enter your choice (1-3):"))
            if user_choice == 1:
                self.display_new_event_menu()
            elif user_choice == 2:
                self.display_edit_existing_events_menu()
            elif user_choice == 3:
                self.display_link_event_menu()
            elif user_choice == 4:
                self._campaign_factory.current_campaign.events = self._events_factory.events_tree
                self._campaign_factory.save_campaign()
                return
            else:
                print("Invalid choice, please try again.")

    def display_new_event_menu(self):
        print("Creating new event...")
        # @TODO: exception handling
        description = input("Enter small event description (max 15 chars) here: ")
        dialogue = input("Enter event dialogue here: ")
        self._events_factory.create_event(description, dialogue)
        self._campaign_factory.current_campaign.events = self._events_factory.events_tree
        self._campaign_factory.save_campaign()

    # honestly could be done so much better...
    def display_edit_existing_events_menu(self):
        # @TODO: exception handling
        # @TODO: use choice_name/choice_description
        while True:
            # print(self._events_manager.events_tree)
            event_id = input("Enter event you'd like to edit: ")
            if event_id not in self._events_factory.events_tree:
                print(f"Event {event_id} not found")
                return
            print(f"Editing event {event_id}")
            # print(self._events_manager.events_tree[event_id])
            user_choice = None
            while user_choice != 3:
                print("1. Edit description\n"
                      # nothing else yet
                      "2. Edit dialogue\n"
                      "3. Cancel edit")
                user_choice = int(input("Enter choice here (1-3): "))
                if user_choice == 1:
                    new_desc = input("Enter new description (max 15 chars): ")
                    self._events_factory.edit_event(event_id, "description", new_desc)
                elif user_choice == 2:
                    new_dialogue = input("Enter new dialogue: ")
                    self._events_factory.edit_event(event_id, "dialogue", new_dialogue)
                # @TODO: implement deleting link between events
                elif user_choice == 3:
                    return
                else:
                    print("Invalid choice please try again.")
                self._campaign_factory.current_campaign.events = self._events_factory.events_tree
                self._campaign_factory.save_campaign()
                print("Edit is done")

    def display_link_event_menu(self):
        print("Linking events...")
        input1 = int(input("Enter first event id: "))
        input2 = int(input("Enter second event id: "))
        self._events_factory.link_event(input1, input2)
        self._campaign_factory.current_campaign.events = self._events_factory.events_tree
        self._campaign_factory.save_campaign()

    # Edit events stuff end =================================

    # def edit_campaign_name_menu(self):
    #     while True:
    #         try:
    #             user_input = input(output.campaign_name_prompt()).strip()
    #             if len(user_input) == 0:
    #                 print("Name cannot be empty, please try again.")
    #             elif user_input.lower() == BACK_KEYWORD:
    #                 break
    #             else:
    #                 self._campaign_manager.rename_campaign(user_input)
    #                 self._campaign_manager.save_campaign()
    #                 break
    #         except ValueError:
    #             print("Name cannot be empty, please try again.")
    #         except OSError:
    #             print(output.invalid_OS_filename(user_input))
    #         except fb.ForbiddenFilenameCharsError:
    #             print(output.invalid_chars_campaign_name(user_input))
                

    # generic function to change any property in campaign
    def _change_campaign_property_menu(self, campaign_prop, prop_name: str, display_prop: str) -> None:
        while True: 
            try:
                print(f"Current {display_prop}: {getattr(campaign_prop, prop_name)}")
                user_input = input(f'Enter new {display_prop}: ')

                if len(user_input) == 0:
                        print("Input cannot be empty, please try again.")
                elif user_input.lower() == BACK_KEYWORD:
                    break
                else:

                    self._campaign_factory.rename_campaign(user_input)
                    self._campaign_factory.save_campaign()
                    break
            except OSError:
                print(output.invalid_OS_filename(user_input))
            except fb.ForbiddenFilenameCharsError:
                print(output.invalid_chars_campaign_name(user_input))

    def display_player_menu(self):
        while True:
            print("You are in player mode. Choices:")
            print("1. Play campaign")
            print("2. Return to main menu")
            try:
                user_choice = int(input("Enter your choice (1-2):"))
                if user_choice == 1:
                    self.display_play_existing_campaigns_menu()
                    break
                elif user_choice == 2:
                    self.display_main_menu()
                    break
                else:
                    print("Invalid choice, please try again.")
            except ValueError:
                print(output.invalid_choice_int_expected())

    def manage_campaign_players(self):
        while True:
            print(f" --Player Character List-- ")
            for index, player in enumerate(self._campaign_factory.current_campaign.player_list):
                print(f"{index + 1}. {player.name}")
            player_index = int(
                input(f"Enter your choice (1-{len(self._campaign_factory.current_campaign.player_list)}):")) - 1
            if 0 <= player_index <= (len(self._campaign_factory.current_campaign.player_list)):
                self.manage_single_campaign_player(player_index)
                break
            else:
                print("Invalid choice, please try again.")

    def manage_single_campaign_player(self, player_index):
        while True:
            print(f" --Player Character Details-- ")
            print(f"{self._campaign_factory.current_campaign.player_list[player_index]}")
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
                self._change_campaign_property(self._campaign_factory.current_campaign.player_list[player_index]
                                               , "name",
                                               self._campaign_factory.current_campaign.player_list[player_index].name
                                               , "name")
                # self._campaign_manager.current_campaign.player_list[player_index].name = new_name
                continue
            if user_choice == 2:
                self._change_campaign_property(self._campaign_factory.current_campaign.player_list[player_index]
                                          , "description",
                                          self._campaign_factory.current_campaign.player_list[player_index].description
                                          , "description")
                continue
            if user_choice == 3:
                self._change_campaign_property(self._campaign_factory.current_campaign.player_list[player_index], "base_hp",
                                               self._campaign_factory.current_campaign.player_list[player_index].base_hp
                                               , "base hit points")
                continue
            if user_choice == 4:
                self._change_campaign_property(self._campaign_factory.current_campaign.player_list[player_index], "base_atk",
                                               self._campaign_factory.current_campaign.player_list[player_index].base_atk
                                               , "base attack")
                continue
            if user_choice == 5:
                self._change_campaign_property(self._campaign_factory.current_campaign.player_list[player_index], "base_spd",
                                               self._campaign_factory.current_campaign.player_list[player_index].base_spd
                                               , "base speed")
                continue
            if user_choice == 6:
                self._change_campaign_property(self._campaign_factory.current_campaign.player_list[player_index]
                                          , "exp_per_lvl_up",
                                          self._campaign_factory.current_campaign.player_list[player_index].exp_per_lvl_up
                                          , "level up experience")
                continue
            if user_choice == 7:
                self._change_campaign_property(self._campaign_factory.current_campaign.player_list[player_index], "max_lvl",
                                               self._campaign_factory.current_campaign.player_list[player_index].max_lvl
                                               , "max level")
                continue
            if user_choice == 8:
                self._change_campaign_property(self._campaign_factory.current_campaign.player_list[player_index], "hp_mod",
                                               self._campaign_factory.current_campaign.player_list[player_index].hp_mod
                                               , "hit point gain per level")
                continue
            if user_choice == 9:
                self._change_campaign_property(self._campaign_factory.current_campaign.player_list[player_index], "atk_mod",
                                               self._campaign_factory.current_campaign.player_list[player_index].atk_mod
                                               , "attack gain per level")
                continue
            if user_choice == 10:
                self._change_campaign_property(self._campaign_factory.current_campaign.player_list[player_index], "spd_mod",
                                               self._campaign_factory.current_campaign.player_list[player_index].spd_mod
                                               , "speed gain per level")
                continue
            if user_choice == 12:
                break
            else:
                print("Invalid choice, please try again.")

    def display_play_existing_campaigns_menu(self):
        while True:
            try:
                self._campaign_factory.load_campaigns()
                choice_count = self.display_campaign_list_choices()
                user_choice = int(input(f"Enter your choice (1-{1 + choice_count}):"))
                if choice_count + 1 > user_choice > 0:
                    self._campaign_factory.set_current_campaign(user_choice - 1)
                    # print(f'--*{self._campaign_manager.current_campaign.name}*--')
                    # self.display_edit_campaign_menu(False)
                    print(f"Playing {self._campaign_factory.current_campaign.name} Campaign")
                    # self._campaign_manager.start_campaign()
                    continue
                elif user_choice == 1 + choice_count:
                    # self.display_editor_menu()
                    break
                else:
                    print("Invalid choice, please try again.")
            except ValueError:
                print(output.invalid_choice_int_expected())

        while True:
            choice_count = self.display_campaign_list_choices()
            user_choice = int(input(f"Enter your choice (1-{1 + choice_count}):"))
            if choice_count + 1 > user_choice > 0:
                # @TODO: change to use CampaignManager
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
                break
            elif user_choice == 3:
                self.use_item_menu()
                break
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
    menu = UserMenu()
    menu.display_main_menu()
