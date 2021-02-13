class Automate:

    def __init__(self, alfabet):
        self.transitions = dict()
        self.finalStates = set()
        self.alfabet = alfabet

    def setStates(self, states):
        self.states = set(states)

    def setInitState(self, state):
        if(state in self.states):
            self.initState = state
        else:
            raise ValueError("This state doesn't exist")

    def setFinalState(self, states):
        states = set(states)

        for state in states:
            if state in self.states:
                if state not in self.finalStates:
                    self.finalStates.add(state)

            else:
                raise ValueError("This state doesn't exists")

    def createTransition(self, origin, destiny, symbol):
        if(
                origin not in self.states or
                symbol not in self.alfabet or
                destiny not in self.states):
            raise ValueError("Error")

        self.transitions[(origin, symbol)] = destiny

    def run(self, chain):
        self.currentState = self.initState

        for symbol in chain:
            currentValue = self.transitions[(self.currentState, symbol)]

            self.currentState = currentValue

        if(self.currentState not in self.finalStates):
            raise ValueError("This chain not accepted")


automate = Automate("ab")
automate.setStates(['q1', 'q2'])
automate.setInitState('q1')
automate.setFinalState(['q1'])

automate.createTransition('q1', 'q2', 'a')
automate.createTransition('q2', 'q1', 'a')
automate.createTransition('q1', 'q1', 'b')
automate.createTransition('q2', 'q2', 'b')

chain = "aaaaabaabbbac"

try:
    automate.run(chain)

    print("Chain accepted!")
except ValueError as err:
    print(err)
except KeyError as err:
    print("Transition not found " + str(err))
