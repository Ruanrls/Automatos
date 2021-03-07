import json


class Anfd:
    def __init__(self, alfabet):
        self.alfabet = alfabet
        self.transitions = dict()
        self.states = set()
        self.init_state = None
        self.final_states = set()

    def CreateStates(self, states):
        self.states = set(states)

    def SetInitState(self, state):
        if state in self.states:
            self.init_state = state
        else:
            self.ThrowError(f"Can't find {state} state in states!")

    def SetFinalStates(self, states):
        for state in states:
            if state in self.states:
                self.final_states.add(state)
            else:
                self.ThrowError(f"This state {state} isn't in states")

    def ValidadeString(self, chain):
        chain = set(chain)
        for symbol in chain:
            if symbol not in self.alfabet:
                self.ThrowError(f"This chain are not suportable ({symbol})")

    def CreateTransition(self, transitions):
        if(
                transitions['origin'] not in self.states or
                transitions['symbol'] not in self.alfabet or
                any([destiny not in self.states for destiny in transitions['destiny']])):
            self.ThrowError("Error")

        index = transitions['origin'] + ";" + transitions['symbol']
        self.transitions[index] = transitions['destiny']

    def Run(self, chain):
        self.ValidadeString(chain)
        self.current_states = [self.init_state]

        for symbol in chain:
            current_values = []
            for state in self.current_states:
                try:
                    current_values.extend(
                        self.transitions[state + ';' + symbol])
                except KeyError:
                    continue
            self.current_states = current_values

        any_valid = any([x in self.final_states for x in self.current_states])
        if(not any_valid or len(self.final_states) == 0):
            self.ThrowError("This automate is invalid")
        else:
            print("This automate is valid")

    def print(self):
        # Troca as ';' para uma '->'
        def parseString(item):
            return item[0].replace(';', '->') + "=" + ','.join(item[1])

        print("E -> A -> T -> I -> F")
        print(f"E: {', '.join(self.states)}")
        print(f"A: {', '.join(list(self.alfabet))}")
        print(f"I: {self.init_state}")
        print(f"F: {', '.join(self.final_states)}")
        """
        para cada um dos elementos de transitions, jogamos a tupla de chave-valor para a função parse
        string e concatenamos em T
        """
        print("T: " + '   '.join(list(map(parseString, self.transitions.items()))))

    def ThrowError(self, error_name):
        try:
            raise Exception(error_name)
        except Exception as err:
            print(err)

    def copyAutomate(self):
        return self

    def saveAutomate(self):
        automate = {
            "type": "afnd",
            "alfabet": self.alfabet,
            "transitions": self.transitions,
            "states": list(self.states),
            "init_state": self.init_state,
            "final_states": list(self.final_states)
        }

        automate = json.dumps(automate)
        with open('automate_undefined.txt', 'w') as file:
            file.write(automate)

    def readAutomate(self):
        with open('automate_undefined.txt', 'r') as file:
            automate = json.load(file)

        self.alfabet = automate['alfabet']
        self.transitions = dict(automate['transitions'])
        self.states = set(automate['states'])
        self.init_state = automate['init_state']
        self.final_states = set(automate['final_states'])


""" automate = Anfd("01")

automate.CreateStates(['q1', 'q2', 'q3', 'q4'])
automate.SetInitState('q1')
automate.SetFinalStates(['q4'])

automate.CreateTransition(
    {'origin': 'q1', 'destiny': ['q1'], 'symbol': '0'})
automate.CreateTransition(
    {'origin': 'q1', 'destiny': ['q1', 'q2'], 'symbol': '1'})
automate.CreateTransition(
    {'origin': 'q2', 'destiny': ['q3'], 'symbol': '0'})
automate.CreateTransition(
    {'origin': 'q2', 'destiny': ['q3'], 'symbol': '1'})
automate.CreateTransition(
    {'origin': 'q3', 'destiny': ['q4'], 'symbol': '0'})
automate.CreateTransition(
    {'origin': 'q3', 'destiny': ['q4'], 'symbol': '1'})

automate.Run('0100100000000010')
automate.print()
automate.saveAutomate()
automate.readAutomate() """
