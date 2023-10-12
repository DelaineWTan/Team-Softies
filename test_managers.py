from object_classes import DialogueEvent, CombatEvent


if __name__ == '__main__':
    print(f'testing dialogue trees')

    test_event = DialogueEvent("Test Dialogue Event")

    test_event.run_event()
