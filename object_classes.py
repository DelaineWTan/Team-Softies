import abc


class Character:
    name = "Anon"
    base_hp = 10
    base_atk = 5
    base_spd = 5
    description = "blank character."
    ascii_art = "\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣬⡛⣿⣿⣿⣯⢻\n" \
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

    def __init__(self, name: str):
        self.name = name


class Player(Character):
    lvl = 1
    exp = 0
    exp_per_lvl_up = 20
    max_lvl = 10
    hp_mod = 5
    atk_mod = 2
    spd_mod = 1

    description = "The main protagonist of your campaign."

    def __init__(self, name: str):
        super().__init__(name)

    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Level: {self.lvl}, {self.exp_per_lvl_up} exp needed to level up\n"
                f"Hit points (HP): {self.base_hp}, +{self.hp_mod} per level up\n"
                f"Attack (atk): {self.base_atk}, +{self.atk_mod - 1} per level up\n"
                f"Speed (spd): {self.base_spd}, +{self.hp_mod - 1} per level up\n"
                f"{self.description}"
                f"{self.ascii_art}")


class NPC(Character):
    friendly = bool

    def __init__(self, name: str):
        super().__init__(name)


class Item:
    name = ""

    def __init__(self, name: str):
        self.name = name


# class Event:
#     name = ""
#     description = ""
#     next = None
#     outcome = None
#
#     def __init__(self, name, description):
#         self.name = name
#         self.description = description
#
#     def setNextEvent(self, event):
#         self.next = event
#
#     def eventOutcome(self, outcome):  # function will take in a universal object
#         if outcome.type == Event:
#             self.setNextEvent(outcome)
#
#         if outcome.type == Item:
#             pass  # give player an item
#
#         if outcome.type == NPC:
#             pass  # trigger battle!


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


class Campaign:
    # defaults just in case
    _name = "The Stick of Tooth"
    _player = Player("Anon")  # just a single player class
    _short_desc = "some short description idk"

    def __init__(self, name, short_desc = '', sequence_of_events = {}, list_of_PCs = [],
        list_of_NPCs = [], items = []):
        self._name = name
        self._previous_name = name
        self._short_desc = short_desc
        self._events = sequence_of_events
        # @TODO do we want to have potentially more than 1 character per campaign?
        self._PCs = list_of_PCs  # PCs are Characters
        self._NPCs = list_of_NPCs  # list of NPC objects, this can be empty
        self._items = items  # list of item objects, this can be empty

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def previous_name(self):
        return self._previous_name
    
    @previous_name.setter
    def previous_name(self, new_name):
        self._previous_name = new_name

    @property
    def short_desc(self) -> str:
        return self._short_desc

    @short_desc.setter
    def short_desc(self, short_desc):
        self._short_desc = short_desc

    @property
    def player(self) -> Player:
        return self._player

    def __str__(self):
        return (f"The \"{self._name}\" campaign plays as {self._player.name}."
                f" This campaign has {len(self._events)} events, {len(self._NPCs)} characters, and {len(self._items)} "
                f"items.")
