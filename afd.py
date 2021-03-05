import json


class Automate:

    def __init__(self, alfabet):
        self.transitions = dict()
        self.final_states = set()
        self.alfabet = alfabet

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

    def createTransition(self, origin, destiny, symbol):
        if(
                origin not in self.states or
                symbol not in self.alfabet or
                destiny not in self.states):
            raise ValueError("Error")

        self.transitions[origin + ";" + symbol] = destiny

    def run(self, chain):
        try:
            self.current_state = self.init_state

            for symbol in chain:
                current_value = self.transitions[self.current_state + ";" + symbol]
                self.current_state = current_value

            if(self.current_state not in self.final_states):
                raise ValueError("This chain not accepted!")

            print("Chain accepted!")
        except ValueError as err:
            print(err)

        except KeyError as err:
            print("Transition not found " + str(err))

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


automate = Automate("abc")
automate.CreateStates(['q1', 'q2'])
automate.setInitState('q1')
automate.setFinalState(['q1'])

automate.createTransition('q1', 'q2', 'a')
automate.createTransition('q2', 'q1', 'a')
automate.createTransition('q1', 'q1', 'b')
automate.createTransition('q2', 'q2', 'b')

chain = "aaaaabaabbbaa"

automate.saveAutomate()
automate.readAutomate()
automate.print()

automate.run(chain)
