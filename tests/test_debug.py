import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from object_classes import Character, Player, DialogueEvent, Campaign

# Property values for reuse in tests, note that these values are different from the default values
# Test property values for the Player class
TEST_ASCII_ART = "\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣬⡛⣿⣿⣿⣯⢻\n" \
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
TEST_NAME = "John"
TEST_BASE_HP = 20
TEST_BASE_ATK = 10
TEST_BASE_SPD = 2
TEST_DESCRIPTION = "custom character description"
TEST_LVL = 2
TEST_EXP = 5
TEST_EXP_PER_LVL_UP = 50
TEST_MAX_LVL = 15
TEST_HP_MOD = 10
TEST_ATK_MOD = 3
TEST_SPD_MOD = 5

# Test property values for DialogueEvent class
TEST_DIALOGUE_EVENT_ID = 123
TEST_DIALOGUE_EVENT_DESCRIPTION = "dialogue event description"
TEST_DIALOGUE_EVENT_CHOICES = [111, 222, 333]

# Test property values for campaign class
TEST_CAMPAIGN_NAME = "Test Campaign"
TEST_CAMPAIGN_SHORT_DESC = "campaign short description"
TEST_CAMPAIGN_EVENTS = {}
TEST_CAMPAIGN_PLAYER_LIST = []  # Note: add actual player classes
TEST_CAMPAIGN_NPC_LIST = []  # Note: add actual NPC classes
TEST_CAMPAIGN_ITEMS = []  # TODO: add items when Item classes completed


# Create a Character object with specific parameters
def test_character_properties():
    character = Character(name=TEST_NAME, base_hp=TEST_BASE_HP, base_atk=TEST_BASE_ATK,
                          base_spd=TEST_BASE_SPD,
                          description=TEST_DESCRIPTION,
                          ascii_art=TEST_ASCII_ART)

    # Assert that the character's properties match the expected values
    assert character.name == TEST_NAME
    assert character.base_hp == TEST_BASE_HP
    assert character.base_atk == TEST_BASE_ATK
    assert character.base_spd == TEST_BASE_SPD
    assert character.description == TEST_DESCRIPTION
    assert character.ascii_art == TEST_ASCII_ART


# Create a Player object with specific parameters
def test_player_properties():
    player = Player(name=TEST_NAME, base_hp=TEST_BASE_HP, base_atk=TEST_BASE_ATK,
                    base_spd=TEST_BASE_SPD,
                    description=TEST_DESCRIPTION,
                    ascii_art=TEST_ASCII_ART, lvl=TEST_LVL, exp=TEST_EXP,
                    exp_per_lvl_up=TEST_EXP_PER_LVL_UP,
                    max_lvl=TEST_MAX_LVL, hp_mod=TEST_HP_MOD, atk_mod=TEST_ATK_MOD,
                    spd_mod=TEST_SPD_MOD)
    # Assert that the object's inherited properties match the expected values
    assert player.name == TEST_NAME
    assert player.base_hp == TEST_BASE_HP
    assert player.base_atk == TEST_BASE_ATK
    assert player.base_spd == TEST_BASE_SPD
    assert player.description == TEST_DESCRIPTION
    assert player.ascii_art == TEST_ASCII_ART
    # Assert that the object's custom properties match the expected values
    assert player.lvl == TEST_LVL
    assert player.exp == TEST_EXP
    assert player.exp_per_lvl_up == TEST_EXP_PER_LVL_UP
    assert player.max_lvl == TEST_MAX_LVL
    assert player.hp_mod == TEST_HP_MOD
    assert player.atk_mod == TEST_ATK_MOD
    assert player.spd_mod == TEST_SPD_MOD


# Create a DialogueEvent object with specific parameters
def test_dialogue_event_properties():
    dialogue_event = DialogueEvent(event_id=TEST_DIALOGUE_EVENT_ID,
                                   description=TEST_DIALOGUE_EVENT_DESCRIPTION,
                                   choices=TEST_DIALOGUE_EVENT_CHOICES)
    # Assert that the object's custom properties match the expected values
    assert dialogue_event.event_id == TEST_DIALOGUE_EVENT_ID
    assert dialogue_event.description == TEST_DIALOGUE_EVENT_DESCRIPTION
    assert dialogue_event.choices == TEST_DIALOGUE_EVENT_CHOICES


# Create a Campaign object with specific parameters and test them
def test_campaign_properties():
    campaign = Campaign(TEST_CAMPAIGN_NAME, TEST_CAMPAIGN_SHORT_DESC, TEST_CAMPAIGN_EVENTS,
                        TEST_CAMPAIGN_PLAYER_LIST,
                        TEST_CAMPAIGN_NPC_LIST, TEST_CAMPAIGN_ITEMS)
    assert campaign.name == TEST_CAMPAIGN_NAME
    assert campaign.short_desc == TEST_CAMPAIGN_SHORT_DESC
    assert campaign.events == TEST_CAMPAIGN_EVENTS
    assert campaign.player_list == TEST_CAMPAIGN_PLAYER_LIST
    assert campaign.npc_list == TEST_CAMPAIGN_NPC_LIST
    # assert campaign._items_list == test_campaign_items
