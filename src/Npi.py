from collections import deque

class Npi:
    def __init__(self):
        # deque fournit une complexité temporelle O(1) pour les opérations de file
        self.numbers = deque()

    def calculatrice(self, expression):
        
        values = expression.split()
        for value in values:
            if value.isdigit():
                self.numbers.append(int(value))
            else:
                if len(self.numbers) < 2:
                    return "Erreur : Pas assez d'opérandes"
                operande2 = self.numbers.pop()
                operande1 = self.numbers.pop()
                result = self.operate(value, operande1, operande2)
                self.numbers.append(result)

        if len(self.numbers) == 1:
            return self.numbers[0]
        else:
            return "Erreur : Trop d'opérandes"

    def operate(self, operator, operande1, operande2):
        if operator == '+':
            return operande1 + operande2
        elif operator == '-':
            return operande1 - operande2
        elif operator == '*':
            return operande1 * operande2
        elif operator == '/':
            if operande2 == 0:
                raise ValueError("Erreur : Division par zéro")
            else:
                return operande1 / operande2

