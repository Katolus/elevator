import time
from typing import List

from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML

from elevator import Elevator
from elevator import Person
from elevator import Door
from elevator import Direction


bottom_toolbar = HTML(
    'Running elevator program, type <b><style bg="ansired">exit</style></b> to quit the program!'
)
session = PromptSession()


class Program:
    def __init__(self, elevator: Elevator, people: List[Person]) -> None:
        self.elevator: Elevator = elevator
        self.people: List[Person] = people
        self.waiting_for_elevator: List[Person] = people

    def report_status(self) -> None:
        """Prints out the status of the program"""

        def names(people) -> List[str]:
            return [person.name for person in people]

        print(f"The elevator is at {self.elevator.floor} floor.")
        print(f"People waiting for a lift {names(self.waiting_for_elevator)}")
        print(f"People in the elevator {names(self.elevator.people)}")

    def add_person_to_lift(self, person: Person) -> None:
        if not self.elevator.door.is_open:
            self.elevator.open_door()
        self.elevator.people.append(person)
        self.waiting_for_elevator.remove(person)
        print(f"{person.name} has entered the lift at {self.elevator.floor} floor")

    def remove_person_to_lift(self, person: Person) -> None:
        if not self.elevator.door.is_open:
            self.elevator.open_door()
        self.elevator.people.remove(person)

        # If there are not people in the lift, it is not moving nowhere
        if not self.elevator.people:
            self.elevator.moving_queue = []
            self.elevator.moving_to = None
        print(f"{person.name} has left the lift at {self.elevator.floor} floor")

    def next(self) -> None:
        # For people in the elevator, check if their current floor
        for person in self.elevator.people:
            if person.exit_floor == self.elevator.floor:
                return self.remove_person_to_lift(person)

        # Move people from outside into the elevator
        for person in self.waiting_for_elevator:
            if person.enter_floor == self.elevator.floor:
                return self.add_person_to_lift(person)

        if self.elevator.door.is_open:
            return self.elevator.close_door()

        # Action elevator
        if self.elevator.people:
            return self.elevator.move()

        # If not in move and people waiting, move the lift to a place
        if self.waiting_for_elevator:
            first_waiting = self.waiting_for_elevator[0]
            if not self.elevator.moving_to:
                self.elevator.moving_to = first_waiting.enter_floor
            self.elevator.move()

    def handle_input(self, answer: str) -> None:
        """
        A method that handles the input and therefore program progress 
        """
        answer = answer.lower()
        if answer in ["", "next"]:
            self.next()
        elif answer in ["new"]:
            self.enter_a_person()
        elif answer in ["s", "status"]:
            self.report_status()
        else:
            print(f"No action for '{answer}'")

    def enter_a_person(self) -> None:
        """
        On being called takes input and adds a person to the waiting people
        """
        name = session.prompt("> ", bottom_toolbar=HTML("Enter a person's name"))
        enter_floor = session.prompt(
            "> ", bottom_toolbar=HTML("The floor they called the elevator")
        )
        exit_floor = session.prompt(
            "> ", bottom_toolbar=HTML("The floor they need to exit")
        )
        self.people.append(Person(name, enter_floor, exit_floor))


scenario_1 = Program(
    elevator=Elevator(-1, 4),
    people=[
        Person("John", 0, 3),
        Person("Jack", 0, 4),
        Person("Jackson", 2, -1),
        Person("Janet", 2, 3),
    ],
)


# Scenario at which the first person is not at the ground floor
scenario_2 = Program(
    elevator=Elevator(-3, 5),
    people=[
        Person("John", 1, 3),
        Person("Jack", 0, -2),
        Person("Jackson", 2, -1),
        Person("Janet", 2, 3),
    ],
)


if __name__ == "__main__":
    program = scenario_2

    while True:
        answer = session.prompt("> ", bottom_toolbar=bottom_toolbar)
        if answer == "exit":
            break
        try:
            program.handle_input(answer=answer)
        except ValueError as error:
            print(error)

        # Avoid cooking CPU
        time.sleep(0.01)

