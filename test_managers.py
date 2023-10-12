from object_classes import Event, DialogueEvent, CombatEvent

if __name__ == '__main__':
    test_event = DialogueEvent("Test Dialogue Event")
    test_combat_event = CombatEvent("Test Combat Event")

    test_event.run_event()
    test_combat_event.run_event()
    print(f'Welcome to our text-based RPG maker!')
