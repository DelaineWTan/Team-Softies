from object_classes import DialogueEvent
from manager_classes import EventManager

if __name__ == '__main__':
    print(f'testing dialogue trees\n')

    description = ("Shlink the princess is in another"
                   " castle! I know you did all that shit but"
                   " sorry about that buckaroo xDDDDDD")

    event_1 = DialogueEvent(1, description, [2, 3])

    event_2 = DialogueEvent(2, description, [4])

    event_3 = DialogueEvent(3, description, [])

    event_4 = DialogueEvent(4, description, [])

    print(event_1)
    print(event_2)
    print(event_3)
    print(event_4)