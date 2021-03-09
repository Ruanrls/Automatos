from afd import Afd
from afnd import Anfd
from multiplication import Multiplicator

chain = "aababbaaaababababa"

afd = Afd("")
print("\nLendo um automato de automate.json: ")
afd.readAutomate()
afd.print()

print(f"\nRodando a cadeia {chain}")
afd.run(chain)

print("\nMinimizando automato: ")
afd.Minimize()
afd.print()

print("\nRodando novamente")
afd.run(chain)

print("\nCriando um automato auxiliar de alfabeto ab")
afd_b = Afd("ab")
afd_b.CreateStates(['q6', 'q7', 'q8', 'q9'])
afd_b.setInitState('q6')
afd_b.setFinalState(['q6', 'q9'])
afd_b.createTransition(
    {'origin': 'q6', 'destiny': 'q7', 'symbol': 'b'})
afd_b.createTransition(
    {'origin': 'q6', 'destiny': 'q8', 'symbol': 'a'})
afd_b.createTransition(
    {'origin': 'q7', 'destiny': 'q7', 'symbol': 'a'})
afd_b.createTransition(
    {'origin': 'q7', 'destiny': 'q6', 'symbol': 'b'})
afd_b.createTransition(
    {'origin': 'q8', 'destiny': 'q9', 'symbol': 'a'})
afd_b.createTransition(
    {'origin': 'q8', 'destiny': 'q9', 'symbol': 'b'})
afd_b.createTransition(
    {'origin': 'q9', 'destiny': 'q8', 'symbol': 'a'})
afd_b.createTransition(
    {'origin': 'q9', 'destiny': 'q8', 'symbol': 'b'})
afd_b.print()

print("\nRodando a cadeia no segundo automato")
afd_b.run(chain)

print("\nVerificando a equivalência dos automatos")
afd.DoubleEquivalence(afd_b)

print("\nMultiplicando os automatos")
multiplicator = Multiplicator(afd, afd_b)
multiplicator.print()
