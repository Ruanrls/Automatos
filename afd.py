import json


class Afd:
    def __init__(self, alfabet):
        self.transitions = dict()
        self.final_states = set()
        self.alfabet = alfabet

    def ThrowError(self, error_name):
        try:
            raise Exception(error_name)
        except Exception as err:
            print(err)

    def CreateStates(self, states):
        self.states = set(states)

    def setInitState(self, state):
        if(state in self.states):
            self.init_state = state
        else:
            raise ValueError("This state doesn't exist")

    def setFinalState(self, states):
        states = set(states)

        for state in states:
            if state in self.states:
                if state not in self.final_states:
                    self.final_states.add(state)
            else:
                raise ValueError("This state doesn't exists")

    def CheckFinalState(self, x):
        return x in self.final_states

    def createTransition(self, transition):
        if(
                transition['origin'] not in self.states or
                transition['symbol'] not in self.alfabet or
                transition['destiny'] not in self.states):
            raise ValueError("Error")

        self.transitions[transition['origin'] + ";" +
                         transition['symbol']] = transition['destiny']

    def RemoveUnusedStates(self):
        current_state = self.init_state
        states_used = [current_state]

        for state in states_used:
            for letter in self.alfabet:
                try:
                    destiny = self.transitions[state + ';' + letter]
                except:
                    self.ThrowError(
                        "This automate isn't complete, can't continue")
                    exit(0)

                if destiny not in states_used:
                    states_used.append(destiny)

        if(len(self.states) == len(states_used)):
            print("Already minimized!")
            return

        self.states = states_used
        states = self.final_states
        for state in list(states):
            if state not in states_used:
                self.final_states.remove(state)

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

    def DoubleEquivalence(self, another_automate):
        aux_automate = self

        aux_automate.states.update(another_automate.states)
        aux_automate.final_states.update(another.final_states)
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

    def run(self, chain):
        try:
            self.current_state = self.init_state
            for symbol in chain:
                current_value = self.transitions[self.current_state + ";" + symbol]
                self.current_state = current_value

            if(self.current_state not in self.final_states):  # Estado de não aceitação
                self.ThrowError(
                    f"This {self.current_state} isn't a final state")
                return

            print("Chain accepted!")
        except KeyError:
            print(
                "this automate isn't complete, the final state is a non-acceptance state")

        except Exception as err:
            print("This chain is not accepted! - " + str(err))

    """ 
        Utils methods
    """

    def copyAutomate(self):
        return self

    def saveAutomate(self):
        automate = {
            "type": "afd",
            "alfabet": self.alfabet,
            "transitions": self.transitions,
            "states": list(self.states),
            "init_state": self.init_state,
            "final_states": list(self.final_states)
        }

        automate = json.dumps(automate)
        with open('automate.txt', 'w') as file:
            file.write(automate)

    def readAutomate(self):
        with open('automate.txt', 'r') as file:
            automate = json.load(file)

        self.alfabet = automate['alfabet']
        self.transitions = dict(automate['transitions'])
        self.states = set(automate['states'])
        self.init_state = automate['init_state']
        self.final_states = set(automate['final_states'])

    def print(self):

        # Troca as ';' para uma '->'
        def parseString(item):
            return item[0].replace(';', '->') + "=" + item[1]

        print("E -> A -> T -> I -> F")
        print("E: " + ', '.join(self.states))
        print("A: " + ', '.join(list(self.alfabet)))
        print("I: " + self.init_state)
        print("F: " + ', '.join(self.final_states))
        """
        para cada um dos elementos de transitions, jogamos a tupla de chave-valor para a função parse
        string e concatenamos em T
        """
        print("T: " + '   '.join(list(map(parseString, self.transitions.items()))))

# automate = Afd("ab")
# automate.CreateStates(['q0', 'q1', 'q2', 'q3', 'q4', 'q5'])
# automate.setInitState('q0')
# automate.setFinalState(['q0', 'q4', 'q5'])

# automate.createTransition({'origin': 'q0', 'destiny': 'q1', 'symbol': 'b'})
# automate.createTransition({'origin': 'q0', 'destiny': 'q2', 'symbol': 'a'})
# automate.createTransition({'origin': 'q1', 'destiny': 'q1', 'symbol': 'a'})
# automate.createTransition({'origin': 'q1', 'destiny': 'q0', 'symbol': 'b'})
# automate.createTransition({'origin': 'q2', 'destiny': 'q4', 'symbol': 'a'})
# automate.createTransition({'origin': 'q2', 'destiny': 'q5', 'symbol': 'b'})
# automate.createTransition({'origin': 'q3', 'destiny': 'q5', 'symbol': 'a'})
# automate.createTransition({'origin': 'q3', 'destiny': 'q4', 'symbol': 'b'})
# automate.createTransition({'origin': 'q4', 'destiny': 'q2', 'symbol': 'b'})
# automate.createTransition({'origin': 'q4', 'destiny': 'q3', 'symbol': 'a'})
# automate.createTransition({'origin': 'q5', 'destiny': 'q2', 'symbol': 'a'})
# automate.createTransition({'origin': 'q5', 'destiny': 'q3', 'symbol': 'b'})

# automate.saveAutomate()
# automate.readAutomate()
# # automate.Minimize()
# automate.run("aaaaabaabbbaaaaaaa")
# # automate.print()

# print('\n')

# another = Afd("ab")
# another.CreateStates(['q6', 'q7', 'q8', 'q9'])
# another.setInitState('q6')
# another.setFinalState(['q6', 'q9'])

# another.createTransition({'origin': 'q6', 'destiny': 'q7', 'symbol': 'b'})
# another.createTransition({'origin': 'q6', 'destiny': 'q8', 'symbol': 'a'})
# another.createTransition({'origin': 'q7', 'destiny': 'q7', 'symbol': 'a'})
# another.createTransition({'origin': 'q7', 'destiny': 'q6', 'symbol': 'b'})
# another.createTransition({'origin': 'q8', 'destiny': 'q9', 'symbol': 'a'})
# another.createTransition({'origin': 'q8', 'destiny': 'q9', 'symbol': 'b'})
# another.createTransition({'origin': 'q9', 'destiny': 'q8', 'symbol': 'a'})
# another.createTransition({'origin': 'q9', 'destiny': 'q8', 'symbol': 'b'})
# another.Minimize()
# another.run("aaaaabaabbbaaaaaaa")
# # another.print()

# automate.DoubleEquivalence(another)
