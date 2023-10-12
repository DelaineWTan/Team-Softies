from EditorObjects import *


campaign_list = [Campaign("The Eternity Terrain"), Campaign("The Demon Forest"), Campaign("The Burning Land")]


def display_main_menu():
    while True:
        print("1. Editor mode")
        print("2. Player mode")

        user_choice = int(input("Enter your choice (1-2):"))
        if user_choice == 1:
            display_editor_menu()
            break
        elif user_choice == 2:
            display_player_menu()
            break
        else:
            print("Invalid choice, please try again.")


def display_editor_menu():
    while True:
        print("You are in editor mode. Choices:")
        print("1. Create new campaign")
        print("2. Select existing campaign")
        print("3. Return to main menu")
        user_choice = int(input("Enter your choice (1-3):"))
        if user_choice == 1:
            display_new_campaign_menu()
            break
        elif user_choice == 2:
            display_edit_existing_campaigns_menu()
            break
        elif user_choice == 3:
            display_main_menu()
            break
        else:
            print("Invalid choice, please try again.")


def display_new_campaign_menu():
    while True:
        user_input = input("Enter new campaign name:")
        if len(user_input) == 0:
            print("Name cannot be empty, please try again.")
        else:
            newCampaign = Campaign(user_input)  # generate new campaign object
            campaign_list.append(newCampaign)
            print(f"New campaign created: {newCampaign.name}")
            display_edit_campaign_menu(newCampaign)
            break


def display_campaign_list_choices():
    print("Campaign list:")
    choice_count = 0
    if campaign_list.count == 0:
        print("No campaigns available.")
    else:
        for index, campaign in enumerate(campaign_list):
            choice_count += 1
            print(f"{index + 1}. {campaign.name}")
    print(f"{1 + choice_count}. Back")
    return choice_count


def display_edit_existing_campaigns_menu():
    while True:
        choice_count = display_campaign_list_choices()
        user_choice = int(input(f"Enter your choice (1-{1 + choice_count}):"))
        if choice_count + 1 > user_choice > 0:
            display_edit_campaign_menu(campaign_list[user_choice - 1])
        elif user_choice == 1 + choice_count:
            display_editor_menu()
            break
        else:
            print("Invalid choice, please try again.")


def display_edit_campaign_menu(campaign: Campaign):
    # @TODO implement all these campaign management options
    while True:
        print(f"Editing campaign: {campaign}")
        print("1. Change campaign name")
        print("2. Edit event tree")
        print("3. Manage events")
        print("4. Manage player characters")
        print("5. Manage non-player characters")
        print("6. Manage items")
        print("7. Delete campaign (WARNING: this action is irreversible)")
        print("8. Back")
        user_choice = int(input("Enter your choice (1-8):"))
        if user_choice == 4:
            manage_campaign_players(campaign)
        if 1 <= user_choice <= 6:
            print("Made a valid choice 1-6")
        elif user_choice == 7:
            campaign_list.remove(campaign)
            print(f"Deleted campaign: {campaign}")
            break
        elif user_choice == 8:
            display_edit_existing_campaigns_menu()
            break
        else:
            print("Invalid choice, please try again.")


def manage_campaign_players(campaign: Campaign) -> None:
    while True:
        print(f" --Managing player character-- ")
        print(f"{campaign.player}")
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
            new_name = input("Enter new Name: ")
            campaign.player.name = new_name
            break
        if 2 <= user_choice <= 12:
            break
        else:
            print("Invalid choice, please try again.")




def display_player_menu():
    while True:
        print("You are in player mode. Choices:")
        print("1. Play campaign")
        print("2. Return to main menu")
        user_choice = int(input("Enter your choice (1-2):"))
        if user_choice == 1:
            display_play_existing_campaigns_menu()
            break
        elif user_choice == 2:
            display_main_menu()
            break
        else:
            print("Invalid choice, please try again.")


def display_play_existing_campaigns_menu():
    while True:
        choice_count = display_campaign_list_choices()
        user_choice = int(input(f"Enter your choice (1-{1 + choice_count}):"))
        if choice_count + 1 > user_choice > 0:
            start_campaign(campaign_list[user_choice - 1])
        elif user_choice == 1 + choice_count:
            display_player_menu()
            break
        else:
            print("Invalid choice, please try again.")


def start_campaign(campaign):
    # @TODO properly extract campaign data to start campaign event sequence
    run_combat_event()
    run_choice_event()
    # game ended, return to main menu
    run_last_choice_event()
    print("Campaign ended!")
    print("########################################################################")
    display_main_menu()


# @TODO Fake combat event
def run_combat_event():
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
            use_item_menu()
        elif user_choice == 4:
            print("You fled successfully!")
            break
        else:
            print("Invalid choice, please try again.")


# @TODO fake use item menu
def use_item_menu():
    print("You used a potion and healed 1 hp!")


# @TODO Fake choice event
def run_choice_event():
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
def run_last_choice_event():
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
    display_main_menu()
