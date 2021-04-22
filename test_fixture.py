import pytest


@pytest.fixture()
def moj_pierwszy_fixture():
    print("Wykonuje fixture")


@pytest.mark.usefixtures("moj_pierwszy_fixture")
def test_pierwszy():
    print("Wykonuje test pierwszy\n")


def test_drugi():
    print("Wykonuje test drugi\n")


@pytest.mark.usefixtures("moj_pierwszy_fixture")
def test_trzeci():
    print("Wykonuje test trzeci\n")
