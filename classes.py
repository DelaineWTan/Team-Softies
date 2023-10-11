import abc


class Campaign:
    def __init__(self, name, short_desc):
        self._name = name
        self._short_desc = short_desc
        self._sequence_of_events = {}
        self._list_of_PCs = []  # PCs are Characters
        self._list_of_NPCs = []


# should we even do something like this?
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

