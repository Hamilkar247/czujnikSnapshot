import pytest


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
