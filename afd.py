import json
from copy import deepcopy
from time import sleep
from minimization import Minimize


class Afd(Minimize):
    """ Initialize automate """

    def __init__(self, alfabet):
        self.transitions = dict()
        self.final_states = set()
        self.alfabet = alfabet

    """ Throw errors on screen """

    def ThrowError(self, error_name):
        try:
            raise Exception(error_name)
        except Exception as err:
            print(err)

    """ Create the states of automates (needs to be a list) """

    def CreateStates(self, states):
        self.states = set(states)

    """ Set the init state of automate """

    def setInitState(self, state):
        if(state in self.states):
            self.init_state = state
        else:
            raise ValueError("This state doesn't exist")

    """ Set the final states of automate """

    def setFinalState(self, states):
        states = set(states)

        for state in states:
            if state in self.states:
                if state not in self.final_states:
                    self.final_states.add(state)
            else:
                raise ValueError("This state doesn't exists")

    """ Check if the state passed by parameter is a final state """

    def CheckFinalState(self, x):
        return x in self.final_states

    """ Create one transition of automate """

    def createTransition(self, transition):
        if(
                transition['origin'] not in self.states or
                transition['symbol'] not in self.alfabet or
                transition['destiny'] not in self.states):
            raise ValueError("Error")

        self.transitions[transition['origin'] + ";" +
                         transition['symbol']] = transition['destiny']

    """ Removes the unused states (all that don't have any transition coming in and coming out) """

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

        self.states = set(states_used)
        states = self.final_states
        for state in list(states):
            if state not in states_used:
                self.final_states.remove(state)

    """ Runs the automate, printing if this chain is accepted or no """

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

    """ Return this automate to copy to another variable (recursive copy)"""

    def copyAutomate(self):
        return deepcopy(self)

    """ Saves the automate in a file (automate.txt). Needs to be json"""

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
        with open('automate.json', 'w') as file:
            file.write(automate)

    """ Reads the automate from a file (automate.txt) needs to be json """

    def readAutomate(self):
        with open('automate.json', 'r') as file:
            automate = json.load(file)

        self.alfabet = automate['alfabet']
        self.transitions = dict(automate['transitions'])
        self.states = set(automate['states'])
        self.init_state = automate['init_state']
        self.final_states = set(automate['final_states'])

    """ Print the current automate (transitions, states, init states, final states) """

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

    """ Create 2 automates and make some operations to them (print the results out) """

    def TestCase(self):

        automate = Afd("ab")
        automate.CreateStates(['q0', 'q1', 'q2', 'q3', 'q4', 'q5'])
        automate.setInitState('q0')
        automate.setFinalState(['q0', 'q4', 'q5'])
        print("\nCreated automate...")

        automate.createTransition(
            {'origin': 'q0', 'destiny': 'q1', 'symbol': 'b'})
        automate.createTransition(
            {'origin': 'q0', 'destiny': 'q2', 'symbol': 'a'})
        automate.createTransition(
            {'origin': 'q1', 'destiny': 'q1', 'symbol': 'a'})
        automate.createTransition(
            {'origin': 'q1', 'destiny': 'q0', 'symbol': 'b'})
        automate.createTransition(
            {'origin': 'q2', 'destiny': 'q4', 'symbol': 'a'})
        automate.createTransition(
            {'origin': 'q2', 'destiny': 'q5', 'symbol': 'b'})
        automate.createTransition(
            {'origin': 'q3', 'destiny': 'q5', 'symbol': 'a'})
        automate.createTransition(
            {'origin': 'q3', 'destiny': 'q4', 'symbol': 'b'})
        automate.createTransition(
            {'origin': 'q4', 'destiny': 'q2', 'symbol': 'b'})
        automate.createTransition(
            {'origin': 'q4', 'destiny': 'q3', 'symbol': 'a'})
        automate.createTransition(
            {'origin': 'q5', 'destiny': 'q2', 'symbol': 'a'})
        automate.createTransition(
            {'origin': 'q5', 'destiny': 'q3', 'symbol': 'b'})

        print("Added transitions")

        automate.print()
        print("Minimizing automate...\n")
        automate.Minimize()
        automate.saveAutomate()
        print("Saved in automate.txt\n")
        sleep(2)
        automate.print()

        chain = "aaaaabaabbbaaaaaaa"
        print(f"Running with chain: {chain}")
        automate.run(chain)

        print('\n')
        print("Creating another automate...\n")
        another = Afd("ab")
        another.CreateStates(['q6', 'q7', 'q8', 'q9'])
        another.setInitState('q6')
        another.setFinalState(['q6', 'q9'])

        another.createTransition(
            {'origin': 'q6', 'destiny': 'q7', 'symbol': 'b'})
        another.createTransition(
            {'origin': 'q6', 'destiny': 'q8', 'symbol': 'a'})
        another.createTransition(
            {'origin': 'q7', 'destiny': 'q7', 'symbol': 'a'})
        another.createTransition(
            {'origin': 'q7', 'destiny': 'q6', 'symbol': 'b'})
        another.createTransition(
            {'origin': 'q8', 'destiny': 'q9', 'symbol': 'a'})
        another.createTransition(
            {'origin': 'q8', 'destiny': 'q9', 'symbol': 'b'})
        another.createTransition(
            {'origin': 'q9', 'destiny': 'q8', 'symbol': 'a'})
        another.createTransition(
            {'origin': 'q9', 'destiny': 'q8', 'symbol': 'b'})
        another.print()
        sleep(2)

        print("\nMinimizing automate\n")
        another.Minimize()
        another.print()

        print(f"Running with: {chain}")
        another.run(chain)

        print("\nChecking equivalence of these automates")
        automate.DoubleEquivalence(another)
