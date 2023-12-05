import sys
import os

# Add the path to your project's root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from object_classes import Character, Player, DialogueEvent, Campaign

# Property values for reuse in tests, note that these values are different from the default values
# Test property values for the Player class
test_ascii_art = "\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣬⡛⣿⣿⣿⣯⢻\n" \
                 "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢻⣿⣿⢟⣻⣿⣿⣿⣿⣿⣿⣮⡻⣿⣿⣧ \n" \
                 "⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣆⠻⡫⣢⠿⣿⣿⣿⣿⣿⣿⣿⣷⣜⢻⣿ \n" \
                 "⣿⣿⡏⣿⣿⣨⣝⠿⣿⣿⣿⣿⣿⢕⠸⣛⣩⣥⣄⣩⢝⣛⡿⠿⣿⣿⣆⢝ \n" \
                 "⣿⣿⢡⣸⣿⣏⣿⣿⣶⣯⣙⠫⢺⣿⣷⡈⣿⣿⣿⣿⡿⠿⢿⣟⣒⣋⣙⠊ \n" \
                 "⣿⡏⡿⣛⣍⢿⣮⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿ \n" \
                 "⣿⢱⣾⣿⣿⣿⣝⡮⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⣋⣻⣿⣿⣿⣿ \n" \
                 "⢿⢸⣿⣿⣿⣿⣿⣿⣷⣽⣿⣿⣿⣿⣿⣿⣿⡕⣡⣴⣶⣿⣿⣿⡟⣿⣿⣿ \n" \
                 "⣦⡸⣿⣿⣿⣿⣿⣿⡛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿ \n" \
                 "⢛⠷⡹⣿⠋⣉⣠⣤⣶⣶⣿⣿⣿⣿⣿⣿⡿⠿⢿⣿⣿⣿⣿⣿⣷⢹⣿⣿ \n" \
                 "⣷⡝⣿⡞⣿⣿⣿⣿⣿⣿⣿⣿⡟⠋⠁⣠⣤⣤⣦⣽⣿⣿⣿⡿⠋⠘⣿⣿ \n" \
                 "⣿⣿⡹⣿⡼⣿⣿⣿⣿⣿⣿⣿⣧⡰⣿⣿⣿⣿⣿⣹⡿⠟⠉⡀⠄⠄⢿⣿ \n" \
                 "⣿⣿⣿⣽⣿⣼⣛⠿⠿⣿⣿⣿⣿⣿⣯⣿⠿⢟⣻⡽⢚⣤⡞⠄⠄⠄⢸⣿ \n"
test_name = "John"
test_base_hp = 20
test_base_atk = 10
test_base_spd = 2
test_description = "custom character description"
test_lvl = 2
test_exp = 5
test_exp_per_lvl_up = 50
test_max_lvl = 15
test_hp_mod = 10
test_atk_mod = 3
test_spd_mod = 5

# Test property values for DialogueEvent class
test_dialogue_event_id = 123
test_dialogue_event_description = "dialogue event description"
test_dialogue_event_choices = [111, 222, 333]

# Test property values for campaign class
test_campaign_name = "Test Campaign"
test_campaign_short_desc = "campaign short description"
test_campaign_events = {}
test_campaign_player_list = []  # Note: add actual player classes
test_campaign_npc_list = []  # Note: add actual NPC classes
test_campaign_items = []  # TODO: add items when Item classes completed


# Create a Character object with specific parameters
def test_character_properties():
    character = Character(name=test_name, base_hp=test_base_hp, base_atk=test_base_atk,
                          base_spd=test_base_spd,
                          description=test_description,
                          ascii_art=test_ascii_art)

    # Assert that the character's properties match the expected values
    assert character.name == test_name
    assert character.base_hp == test_base_hp
    assert character.base_atk == test_base_atk
    assert character.base_spd == test_base_spd
    assert character.description == test_description
    assert character.ascii_art == test_ascii_art


# Create a Player object with specific parameters
def test_player_properties():
    player = Player(name=test_name, base_hp=test_base_hp, base_atk=test_base_atk,
                    base_spd=test_base_spd,
                    description=test_description,
                    ascii_art=test_ascii_art, lvl=test_lvl, exp=test_exp,
                    exp_per_lvl_up=test_exp_per_lvl_up,
                    max_lvl=test_max_lvl, hp_mod=test_hp_mod, atk_mod=test_atk_mod,
                    spd_mod=test_spd_mod)
    # Assert that the object's inherited properties match the expected values
    assert player.name == test_name
    assert player.base_hp == test_base_hp
    assert player.base_atk == test_base_atk
    assert player.base_spd == test_base_spd
    assert player.description == test_description
    assert player.ascii_art == test_ascii_art
    # Assert that the object's custom properties match the expected values
    assert player.lvl == test_lvl
    assert player.exp == test_exp
    assert player.exp_per_lvl_up == test_exp_per_lvl_up
    assert player.max_lvl == test_max_lvl
    assert player.hp_mod == test_hp_mod
    assert player.atk_mod == test_atk_mod
    assert player.spd_mod == test_spd_mod


# Create a DialogueEvent object with specific parameters
def test_dialogue_event_properties():
    dialogue_event = DialogueEvent(event_id=test_dialogue_event_id,
                                   description=test_dialogue_event_description,
                                   choices=test_dialogue_event_choices)
    # Assert that the object's custom properties match the expected values
    assert dialogue_event.event_id == test_dialogue_event_id
    assert dialogue_event.description == test_dialogue_event_description
    assert dialogue_event.choices == test_dialogue_event_choices


# Create a Campaign object with specific parameters and test them
def test_campaign_properties():
    campaign = Campaign(test_campaign_name, test_campaign_short_desc, test_campaign_events,
                        test_campaign_player_list,
                        test_campaign_npc_list, test_campaign_items)
    assert campaign.name == test_campaign_name
    assert campaign.short_desc == test_campaign_short_desc
    assert campaign.events == test_campaign_events
    assert campaign.player_list == test_campaign_player_list
    assert campaign.npc_list == test_campaign_npc_list
    # assert campaign._items_list == test_campaign_items
