import pytest


class klasa_czas:
    def __init__(self):
        import time
        self.czas = time

    def godzina(self):
        return self.czas.strftime("%H:%M:%S")

    def data(self):
        return self.czas.strftime("%D")


@pytest.fixture()
def czas():
    return klasa_czas()


def test_czas_pierwszy(czas):
    print(czas.godzina())
    print(czas.data())


@pytest.fixture()
def moj_pierwszy_fixture(request):
    print("Wykonuje fixture")

    def na_zakonczenie():
        print("Wykonuje po zakończonym teście \n")

    # uwaga nazwa funkcji jako atrybut daj bez nawiasów!
    request.addfinalizer(na_zakonczenie)


@pytest.mark.usefixtures("moj_pierwszy_fixture")
def test_pierwszy():
    print("Wykonuje test pierwszy\n")


def test_drugi():
    print("Wykonuje test drugi\n")


@pytest.mark.usefixtures("moj_pierwszy_fixture")
def test_trzeci():
    print("Wykonuje test trzeci")
    #assert 1 == 2
