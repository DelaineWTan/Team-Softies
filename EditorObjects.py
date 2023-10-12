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
    name = "Untitled Campaign"
    events = []  # empty linked list of event objects
    player = Player("Anon")  # just a single player class
    NPCs = []  # list of NPC objects, this can be empty
    items = []  # list of item objects, this can be empty

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return (f"The \"{self.name}\" campaign plays as {self.player.name}."
                f" This campaign has {len(self.events)} events, {len(self.NPCs)} characters, and {len(self.items)} items.")
