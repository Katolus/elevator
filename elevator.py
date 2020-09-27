from typing import Optional, Set, List


class Direction:
    UP = "UP"
    DOWN = "DOWN"

class Door:
    def __init__(self, is_open: bool = False) -> None:
        self.is_open: bool = is_open

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False


class Elevator:
    def __init__(self, lowest_floor: int, highest_floor: int) -> None:
        self.door: Door = Door()
        self.floor: int = 0  # Starts from ground level
        self.HIGHEST_FLOOR: int = highest_floor
        self.LOWEST_FLOOR: int = lowest_floor
        self.moving_queue: Set[int] = set()
        self.moving_to: Optional[int] = None  # If None it means that the lift is unused
        self.people: List[Person] = []

        self.validate()

    def report_status(self) -> None:
        pass

    def open_door(self):
        print(f"Elevator door have opened")
        self.door.open()

    def close_door(self):
        print(f"Elevator door have closed")
        self.door.close()

    def move(self):
        if self.door.is_open:
            self.door.close()

        print(self.direction)
        if self.direction == Direction.UP:
            self._up_1()
        elif self.direction == Direction.DOWN:
            self._down_1()
        else:
            self.set_direction()

    def set_direction(self):
        """
        A function that picks the direction in which the lift is gonna move.
        """

        def filterUp(floor):
            return floor > self.floor

        def filterDown(floor):
            return floor < self.floor

        if not self.calls:
            return print(f"The elevator is not moving anywhere")

        oldest_request = self.calls[0]
        if oldest_request > self.floor:
            self.moving_queue = list(filter(filterUp, self.calls))
        elif oldest_request < self.floor:
            self.moving_queue = list(filter(filterDown, self.calls))
        else:
            print("Something went wrong")
        self.moving_to = self.moving_queue[-1]
        print(self.moving_to)
        print(self.moving_queue)

    @property
    def calls(self) -> List[int]:
        """
        Returns a list of floors at which people inside the elevator
        want to get out.
        """
        return [person.exit_floor for person in self.people]

    @property
    def direction(self) -> Optional[str]:
        """
        Returns the current direction in which the elvator is
        moving or null if not decided yet.
        """
        if not self.moving_to:
            return None
        if self.moving_to > self.floor:
            return Direction.UP
        if self.moving_to < self.floor:
            return Direction.DOWN
        else:
            print('dsadasdas')

    def get_moving_queue(self, calls: List[int]) -> Set[int]:
        """
        Returns a list of unique floors to stop on.
        """
        move_queue = []
        for call in calls:
            if call > self.floor:
                move_queue.append(call)
        move_queue.sort()
        return set(move_queue)

    def validate(self):
        if type(self.LOWEST_FLOOR) != int or type(self.LOWEST_FLOOR) != int:
            raise ValueError("Invalid lowest floor")
        if self.LOWEST_FLOOR > 0:
            raise ValueError("Invalid lowest floor")
        if self.HIGHEST_FLOOR <= 0:
            raise ValueError("Invalid highest floor")
        if self.LOWEST_FLOOR >= self.HIGHEST_FLOOR:
            raise ValueError("Invalid elevator")

    def _up_1(self):
        if self.door.is_open:
            raise ValueError("Cannot move the elevator if the door is not closed")
        if self.floor + 1 > self.HIGHEST_FLOOR:
            raise ValueError(f"Can't go higher that the {self.HIGHEST_FLOOR} floor")
        self.floor += 1
        print(f"Moved floors {self.floor -1} -> {self.floor}")

    def _down_1(self):
        if self.door.is_open:
            raise ValueError("Cannot move the elevator if the door is not closed")
        if self.floor - 1 < self.LOWEST_FLOOR:
            raise ValueError(f"Can't go lower that the {self.LOWEST_FLOOR} floor")
        self.floor -= 1
        print(f"Moved floors {self.floor + 1} -> {self.floor}")


class Person:
    COUNTER = 0

    def __init__(self, name: str, enter_floor: int, exit_floor: int) -> None:
        self.name = name  # ID, might need to check if unique
        self.enter_floor = int(enter_floor)
        self.exit_floor = int(exit_floor)

        Person.COUNTER += 1
        self.id = Person.COUNTER

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return (
            f"<Person id:{self.id} -> {(self.name, self.enter_floor, self.exit_floor)}"
        )