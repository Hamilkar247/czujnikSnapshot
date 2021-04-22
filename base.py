import logging
#zalozenia
#Założenia do kalkulatora:
#
#    bazuje na kolejności wprowadzania liczb (nie uwzględnia kolejności wykonywania działań),
#    obsługuje liczby ujemne,
#    nie jest zabezpieczony przed dzieleniem przez 0,
#    nie jest zabezpieczony przed wprowadzaniem innych znaków zamiast liczb.

class BasicCalculator:
    def __init__(self):
        logging.root.setLevel(logging.DEBUG)
        self.numbers = []
        self.signs = [] #symbol
        self.result = 0

    def provice_number(self, number):
        self.numbers.append(number)
        if len(self.signs) == 0:
            self.result = number
        else:
            self.result = self.__calculate()

    def provide_operand(self, operand):
        self.signs.append(operand)

    def __calculate(self):
        logging.debug(f"znak {self.signs[-1]}")
        if self.signs[-1] == '+':
            return self.result + self.numbers[-1]
        if self.signs[-1] == '-':
            return self.result - self.numbers[-1]
        if self.signs[-1] == '*':
            return self.result * self.numbers[-1]
        if self.signs[-1] == '/':
            return self.result / self.numbers[-1]

    def show_result(self):
        logging.debug(f"signs {self.signs}")
        logging.debug(f"numbers {self.numbers}")
        self.signs.append('=')
        logging.debug(f"signs {self.signs}")
        sequence = ''
        logging.debug(f"len(self.numbers): {len(self.numbers)}")
        logging.debug(f"range(len(self.numbers)): {range(len(self.numbers))}")
        for i in range(len(self.numbers)):
            logging.debug("ahjo")
            sequence = f"{sequence} : {self.numbers[i]} {self.signs[i]}"
        sequence += str(self.result)
        print(sequence)
        return self.result, sequence
