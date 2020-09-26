import pytest

from elevator.elevator import Elevator


def test_cannot_go_above_highest_floor():
    elevator = Elevator(0, 1)
    elevator._up_1()
    with pytest.raises(ValueError) as error:
        elevator._up_1()
        assert str(error) == "Can't go higher that the 1"

def test_cannot_go_below_lowest_floor():
    elevator = Elevator(0, 1)
    with pytest.raises(ValueError) as error:
        elevator._down_1()
        assert str(error) == "Can't go lower that the 0"
