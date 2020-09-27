import pytest

from elevator import Elevator
from elevator import Door
from elevator import Person


class TestDoor:
    def test_initial(self):
        door = Door()
        assert not door.is_open

    def test_open(self):
        door = Door()
        door.open()
        assert door.is_open

    def test_close(self):
        door = Door(is_open=True)
        assert door.is_open
        door.close()
        assert not door.is_open

class TestElevator:
    def test_invalid_elevator(self):
        Elevator(0, 1)
        with pytest.raises(ValueError):
            Elevator(1, 1)
        with pytest.raises(ValueError):
            Elevator(2, 1)
        with pytest.raises(ValueError):
            Elevator(-3, -2)
        with pytest.raises(ValueError):
            Elevator(1, 2)
        with pytest.raises(ValueError):
            Elevator(-1.2, 1)
        with pytest.raises(ValueError):
            Elevator('ground', 'first')

    def test_cannot_go_above_highest_floor(self):
        elevator = Elevator(0, 1)
        elevator._up_1()
        with pytest.raises(ValueError) as error:
            elevator._up_1()
            assert str(error) == "Can't go higher that the 1"

    def test_cannot_move_if_doors_are_not_closed(self):
        elevator = Elevator(-2, 2)
        elevator._down_1()
        elevator._up_1()
        # Open door
        elevator.door.open()
        with pytest.raises(ValueError) as error:
            elevator._down_1()
        with pytest.raises(ValueError) as error:
            elevator._up_1()
        # Close door 
        elevator.door.close()
        elevator._down_1()
        elevator._up_1()

    def test_cannot_go_below_lowest_floor(self):
        elevator = Elevator(0, 1)
        with pytest.raises(ValueError) as error:
            elevator._down_1()
            assert str(error) == "Can't go lower that the 0"


class TestPerson:
    def test_invalid(self):
        with pytest.raises(TypeError):
            person = Person()

        with pytest.raises(ValueError):
            person = Person('Joe', 'first', 'last')

        # Etc...

    def test_string_values(self):
        person = Person('Jack', '0', -1)
        assert person.enter_floor == 0
        assert person.exit_floor == -1

    def test_increment(self):
        current_count =  Person.COUNTER 
        person = Person('Jess', 0, 1)
        assert Person.COUNTER == current_count + 1

    def test_str(self):
        person = Person('Jess', 0, 1)
        assert str(person) == f"<Person id:{person.id} -> ('Jess', 0, 1)"