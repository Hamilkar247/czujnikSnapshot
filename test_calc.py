from base import BasicCalculator


def test_addition():
    object = BasicCalculator()
    object.provice_number(10)
    object.provide_operand('+')
    object.provice_number(5)
    assert object.show_result()[0] == 15


def test_subtraction():
    object = BasicCalculator()
    object.provice_number(13)
    object.provice_number('-')
    object.provice_number(21)
    assert object.show_result()[0] == -8
