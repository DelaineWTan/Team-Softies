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


class Event:
    name = ""
    description = ""
    next = None
    outcome = None

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def setNextEvent(self, event):
        self.next = event

    def eventOutcome(self, outcome):  # function will take in a universal object
        if outcome.type == Event:
            self.setNextEvent(outcome)

        if outcome.type == Item:
            pass  # give player an item

        if outcome.type == NPC:
            pass  # trigger battle!


class Campaign:
    # defaults just in case
    _name = "The Stick of Tooth"
    _player = Player("Anon")  # just a single player class

    def __init__(self, name, short_desc):
        self._name = name
        self._short_desc = short_desc
        self._events = {}
        # do we want to have potentially more than 1 character per campaign?
        self._PCs = []  # PCs are Characters
        self._NPCs = []  # list of NPC objects, this can be empty
        self._items = []  # list of item objects, this can be empty

    @property
    def name(self) -> str:
        return self._name

    @property
    def short_desc(self) -> str:
        return self._short_desc

    def __str__(self):
        return (f"The \"{self._name}\" campaign plays as {self._player.name}."
                f" This campaign has {len(self._events)} events, {len(self._NPCs)} characters, and {len(self._items)} "
                f"items.")
