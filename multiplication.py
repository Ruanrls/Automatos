class Multiplicator:
    def __init__(self, automate, another_automate):
        if sorted(automate.alfabet) != sorted(another_automate.alfabet):
            print("The alfabets needs to be equals.")
            return

        self.states = set()
        self.final_states = set()
        self.alfabet = automate.alfabet
        self.automate_a = automate
        self.automate_b = another_automate
        self.transitions = dict()
        self.SetStates()
        self.MakeTransitions()
        self.MakeUnion()
        self.MakeIntersection()
        self.MakeDifference()

    def SetStates(self):
        for state_a in self.automate_a.states:
            for state_b in self.automate_b.states:
                append_key = f"{state_a};{state_b}"
                self.states.add(append_key)
                if state_a == self.automate_a.init_state and state_b == self.automate_b.init_state:
                    self.init_state = append_key

    def MakeTransitions(self):
        for state in self.states:
            current_state = state.split(';')
            for key in self.alfabet:
                next_state = []
                next_state.append(
                    self.automate_a.transitions[f"{current_state[0]};{key}"])
                next_state.append(
                    self.automate_b.transitions[f"{current_state[1]};{key}"])
                self.transitions[f"{state};{key}"] = f"{next_state[0]};{next_state[1]}"

    def MakeUnion(self):
        self.union_final_states = set()

        for state in self.states:
            splitted_state = state.split(';')
            for state_a in self.automate_a.final_states:
                if splitted_state[0] == state_a:
                    self.union_final_states.add(state)

            for state_b in self.automate_b.final_states:
                if splitted_state[1] == state_b:
                    self.union_final_states.add(state)

    def MakeIntersection(self):
        self.intersection_states = list(self.union_final_states)

        for state in self.union_final_states:
            splitted_state = state.split(';')

            is_first_in = splitted_state[0] not in self.automate_a.final_states
            is_second_in = splitted_state[1] not in self.automate_b.final_states
            if is_first_in or is_second_in:
                self.intersection_states.remove(state)

    def MakeDifference(self):
        self.different_states = list(self.union_final_states)

        for state in self.union_final_states:
            splitted_state = state.split(';')

            is_first_in = splitted_state[0] in self.automate_a.final_states
            is_second_in = splitted_state[1] not in self.automate_b.final_states
            if not (is_first_in and is_second_in):
                self.different_states.remove(state)

    def print(self):
        print("\nResultant states of multiplication")
        for state in sorted(self.states):
            print(state, end=" ")

        print("\n\nUnion final states")
        for state in sorted(self.union_final_states):
            print(state, end=" ")

        print("\n\nIntersection final states")
        for state in sorted(self.intersection_states):
            print(state, end=" ")

        print("\n\nDifferent final states")
        for state in sorted(self.different_states):
            print(state, end=" ")
