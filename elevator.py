# To be able to type classes defined later in the script
from __future__ import annotations
import sys
from typing import Optional, Set, List, Dict


class Direction:
    UP = "UP"
    DOWN = "DOWN"


class Status:
    FREE = "free"
    MOVING = "moving"


class Controller:
    COUNTER = 0

    def __init__(self) -> None:
        self.elevators: Optional[Dict[int, Elevator]] = {}

    def add_elevator(self, elevator: Elevator) -> None:
        """
        Adds an elevator to a controller.
        """
        Controller.COUNTER += 1
        self.elevators[Controller.COUNTER] = elevator

    @property
    def free_elevators(self) -> List[Elevator]:
        if not self.elevators:
            raise ValueError("No elevators in this controller")
        return [elevator for elevator in self.elevators.values() if elevator.is_free]

    def call_elevator(self, floor):
        """Moves the 'best' elevator into a called floor"""
        # Pick an elevator that is the closest and can travel to this floor
        best_elevator = None
        min_value = sys.maxint
        for elevator in self.free_elevators:
            if elevator.LOWEST_FLOOR <= floor <= elevator.HIGHEST_FLOOR:
                floor_difference = abs(floor - elevator.floor)
                if floor_difference < min_value:
                    min_value = floor_difference
                    best_elevator = elevator
        if not best_elevator:
            return print('No elevator free at the moment')

        # Send an elevator
        best_elevator.move_to(floor)


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

    @property
    def is_free(self) -> bool:
        return not bool(self.moving_to)

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
            return None

    def move_to(self, floor) -> None:
        self.moving_to = floor

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
