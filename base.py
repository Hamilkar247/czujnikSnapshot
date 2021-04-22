
#zalozenia
#Założenia do kalkulatora:
#
#    bazuje na kolejności wprowadzania liczb (nie uwzględnia kolejności wykonywania działań),
#    obsługuje liczby ujemne,
#    nie jest zabezpieczony przed dzieleniem przez 0,
#    nie jest zabezpieczony przed wprowadzaniem innych znaków zamiast liczb.

class BasicCalculator:
    def __init__(self):
        self.number = []
        self.signs = [] #symbol
        self.result = 0

    def provice_number(self.number):
        self.numbers.append(number)
        if len(self.signs) == 0:
            self.result = number
        else:
            self.result = self.__calculate()

    def provide_operand(self, operand):
        self.signs.append(operand)

    def __calculate(self):
        if self.signs[-1] is '+':
            return self.result + self.numbers[-1]
        if self.signs[-1] is '-':
            return self.result - self.numbers[-1]
        if self.signs[-1] is '*':
            return self.result * self.numbers[-1]
        if self.signs[-1] is '/':
            return self.result / self.numbers[-1]

    def show_result(self):
        self.signs.append('=')
        sequence = ''
        for i in range(len(self.numbers)):
            sequence = sequence + '{} {} '.format(Self.numbers[i], self.signs[i])
        sequence += str(self.result)
        print(sequence)
        return self.result, sequence
