import abc


class Character:
    default_ascii_art = "\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣬⡛⣿⣿⣿⣯⢻\n" \
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

    def __init__(self, name: str = "Anon", base_hp: int = 10, base_atk: int = 5, base_spd: int = 5,
                 description: str = "blank character.", ascii_art: str = default_ascii_art):
        self.name = name
        self.base_hp = base_hp
        self.base_atk = base_atk
        self.base_spd = base_spd
        self.description = description
        self.ascii_art = ascii_art


class Player(Character):
    def __init__(self, lvl: int = 1, exp: int = 0, exp_per_lvl_up: int = 20,
                 max_lvl: int = 10, hp_mod: int = 5, atk_mod: int = 2, spd_mod: int = 1, **kwargs):
        super().__init__(**kwargs)
        self.lvl = lvl
        self.exp = exp
        self.exp_per_lvl_up = exp_per_lvl_up
        self.max_lvl = max_lvl
        self.hp_mod = hp_mod
        self.atk_mod = atk_mod
        self.spd_mod = spd_mod

    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Level: {self.lvl}, {self.exp_per_lvl_up} exp needed to level up\n"
                f"Hit points (HP): {self.base_hp}, +{self.hp_mod} per level up\n"
                f"Attack (atk): {self.base_atk}, +{self.atk_mod} per level up\n"
                f"Speed (spd): {self.base_spd}, +{self.hp_mod} per level up\n"
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


class Event(abc.ABC):
    @abc.abstractmethod
    def run_event(self):
        pass


class DialogueEvent(Event):
    def __init__(self, event_id=99999, description="null event", choices=[]):
        self._event_id = event_id
        self._description = description
        # @TODO choices should be event ids plus the text associated with the choice
        if choices is None:
            self._choices = []  # list of next event ids
        else:
            self._choices = choices

    def run_event(self):
        print(self._description)
        print("running the dialogue event idk")

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def event_id(self):
        return self._event_id

    @event_id.setter
    def event_id(self, event_id):
        self._event_id = event_id

    @property
    def choices(self):
        return self._choices

    @choices.setter
    def choices(self, choices):
        self._choices = choices

    def __str__(self):
        event_string = (f"event_id: {self._event_id}\n"
                        f"description: {self._description}\n")
        if len(self._choices) == 0:
            event_string += f"--=== Event End ===--\n"
        elif len(self._choices) == 1:
            event_string += f" > continue\n"
        else:
            for choice in self._choices:
                event_string += f" > choice event id: {choice}\n"

        return event_string


class CombatEvent(Event):
    def __init__(self, description):
        self._description = description  # will the combat event have a description?
        self._list_of_choices = []  # idk

    def run_event(self):
        print(self._description)
        print("running the combat event idk")


class Campaign:
    def __init__(self, name, short_desc="", events={}, player_list=[Player("Anon")],
                 npc_list=[], items=[]):
        self._name = name
        self._previous_name = name
        self._short_desc = short_desc
        self._events = events
        # @TODO do we want to have potentially more than 1 character per campaign?
        self._player_list = player_list  # players are characters
        self._npc_list = npc_list  # list of NPCs, this can be empty
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
    def events(self):
        return self._events

    @events.setter
    def events(self, events):
        self._events = events

    @property
    def player_list(self) -> list[Player]:
        return self._player_list

    @property
    def npc_list(self) -> list[NPC]:
        return self._npc_list



    def __str__(self):
        return (f"Campaign: \"{self._name}\""
                f" This campaign has {len(self._events)} events, {len(self._npc_list)} player characters, "
                f"{len(self._npc_list)} NPC characters, and {len(self._items)} "
                f"items.")
