class Minimize:
    """ Create the minimization table of this automate """

    def CreateMinimizationTable(self):
        self.minimization_table = {}

        for state_y in sorted(self.states):
            for state_x in sorted(self.states):
                if state_x < state_y:
                    list_condition = list(
                        map(self.CheckFinalState, [state_x, state_y]))
                    if not all(list_condition) and any(list_condition):
                        is_equivalent = True
                    else:
                        is_equivalent = False

                    self.minimization_table[f"{state_y};{state_x}"] = is_equivalent

    """ Check non equivalents statuses with  True flag """

    def CheckEquivalents(self):
        self.CreateMinimizationTable()

        for key, value in sorted(self.minimization_table.items()):
            origin, destiny = key.split(';')[0], key.split(';')[1]
            if value == True:
                continue

            for symbol in self.alfabet:
                try:
                    comparison_origin = self.transitions[f"{origin};{symbol}"]
                    comparison_destiny = self.transitions[f"{destiny};{symbol}"]
                except:
                    continue

                if comparison_origin == comparison_destiny:
                    continue
                try:
                    if self.minimization_table[f'{comparison_origin};{comparison_destiny}'] == True:
                        self.minimization_table[f"{origin};{destiny}"] = True
                        break
                except:
                    if self.minimization_table[f'{comparison_destiny};{comparison_origin}'] == True:
                        self.minimization_table[f"{destiny};{origin}"] = True
                        break

    """ Check if the passed automate are equivalent to this one """

    def DoubleEquivalence(self, another_automate):
        aux_automate = self

        aux_automate.states.update(another_automate.states)
        aux_automate.final_states.update(another_automate.final_states)
        aux_automate.transitions.update(another_automate.transitions)

        aux_automate.CheckEquivalents()

        try:
            is_equivalent = aux_automate.minimization_table[
                f'{self.init_state};{another_automate.init_state}']
        except:
            is_equivalent = aux_automate.minimization_table[
                f'{another_automate.init_state};{self.init_state}']

        if is_equivalent == False:
            print("Equivalent automates")
            return
        else:
            print("Not equivalent automates")

    """  Minimize the automate to your minimal form """

    def Minimize(self):
        self.CheckEquivalents()

        for block in self.minimization_table.items():
            if block[1] == False:
                keys = list(self.transitions.keys())
                for key in keys:
                    if self.transitions[key] == block[0].split(';')[1]:
                        self.transitions[key] = block[0].split(';')[0]

                    if key.split(';')[0] == block[0].split(';')[1]:
                        self.transitions.pop(key)

        self.RemoveUnusedStates()
